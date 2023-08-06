from typing import Tuple, Optional, Union, Callable
import torch
from tqdm import tqdm
from functools import partial

from alpaca.ue.base import UE
from alpaca.models import EnsembleConstructor
from alpaca.ue import acquisitions
from alpaca.utils.model_builder import uncertainty_mode, inference_mode

__all__ = ["EnsembleMCDUE"]


class Ensemble(UE):
    """
    Estimate uncertainty for samples with Ensemble and MCDUE approach
    """

    _name = "EnsembleMCDUE"
    _default_acquisition = partial(acquisitions.std)

    def __init__(
        self,
        *args,
        acquisition: Optional[Union[str, Callable]] = None,
        reduction=None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._create_model_from_list()
        self.reduction = reduction

        # set acquisition strategy
        if acquisition is None:
            # set default acquisiiton strategy if not given
            # defined as the attribute for each subclass
            self._acquisition = self._default_acquisition
        elif callable(acquisition):
            self._acquisition = acquisition
        else:
            try:
                self._acquisition = acquisitions.acq_reg[acquisition]
            except KeyError:
                # TODO: move this to exceptions list
                raise ValueError("The given acquisition strategy doesn't exist")

    def __call__(self, X_pool: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        mcd_runs = None
        self.net = uncertainty_mode(self.net)
        with torch.no_grad():
            # Some mask needs first run without dropout, i.e. decorrelation mask
            self.net(X_pool, reduction=self.reduction)

            # Get mcdue estimation
            for nn_run in tqdm(range(self.nn_runs), total=self.nn_runs, desc=self.desc):
                prediction = self.net(X_pool, reduction=self.reduction)
                mcd_runs = (
                    prediction.flatten().cpu()[None, ...]
                    if mcd_runs is None
                    else torch.cat(
                        [mcd_runs, prediction.flatten().cpu()[None, ...]], dim=0
                    )
                )

        predictions = mcd_runs.mean(dim=0)

        # save `mcf_runs` stats
        if self.keep_runs is True:
            self._mcd_runs = mcd_runs
        self.net = inference_mode(self.net)
        return predictions, self._acquisition(mcd_runs)

    def _create_model_from_list(self):
        self.net = EnsembleConstructor(self.net)
        self.net.eval()
