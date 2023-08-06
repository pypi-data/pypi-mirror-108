from .optimizer import Optimizer
from .cross_validation import CrossValidationEstimator
from .ensemble_optimizer import EnsembleOptimizer
from .fit_methods import fit, available_fit_methods
from .oi import _read_pickle as read_summary


__all__ = ['fit',
           'read_summary',
           'available_fit_methods',
           'Optimizer',
           'EnsembleOptimizer',
           'CrossValidationEstimator']

__project__ = 'trainstation'
__description__ = 'Convenient training of linear models'
__copyright__ = '2021'
__license__ = 'MIT'
__version__ = '0.2'
__maintainer__ = 'trainstation developers group'
__url__ = 'http://trainstation.materialsmodeling.org/'
