
__author__ = 'Kevin Chen'
__status__ = 'Development'

from unittest import TestCase
from MathematicaToLaTeX import replace_vars

SYMBOLS = {
    'Alpha': 'alpha', 'Beta': 'beta', 'Gamma': 'gamma', 'Delta': 'delta',
    'Epsilon': 'epsilon', 'Zeta': 'zeta', 'Eta': 'eta', 'Theta': 'theta',
    'Iota': 'iota', 'Kappa': 'kappa', 'Lambda': 'lambda', 'Mu': 'mu',
    'Nu': 'nu', 'Xi': 'xi', 'Omicron': 'o', 'Pi': 'pi', 'Rho': 'rho',
    'Sigma': 'sigma', 'Tau': 'tau', 'Upsilon': 'upsilon', 'Phi': 'phi',
    'Chi': 'chi', 'Psi': 'phi', 'Omega': 'omega',

    'CapitalAlpha': ' A', 'CapitalBeta': ' B', 'CapitalGamma': 'Gamma',
    'CapitalDelta': 'Delta', 'CapitalEpsilon': 'E', 'CapitalZeta': ' Z',
    'CapitalEta': ' H', 'CapitalTheta': 'Theta', 'CapitalIota': ' I',
    'CapitalKappa': 'K', 'CapitalLambda': 'Lambda', 'CapitalMu': ' M',
    'CapitalNu': ' N', 'CapitalXi': 'Xi', 'CapitalOmicron': 'O',
    'CapitalPi': 'Pi', 'CapitalRho': ' P', 'CapitalSigma': 'Sigma',
    'CapitalTau': ' T', 'CapitalUpsilon': ' Y', 'CapitalPhi': 'Phi',
    'CapitalChi': ' X', 'CapitalPsi': 'Psi', 'CapitalOmega': 'Omega',

    'CurlyEpsilon': 'varepsilon', 'CurlyTheta': 'vartheta',
    'CurlyKappa': 'varkappa', 'CurlyPi': 'varpi', 'CurlyRho': 'varrho',
    'FinalSigma': 'varsigma', 'CurlyPhi': 'varphi',
    'CurlyCapitalUpsilon': 'varUpsilon',

    'Aleph': 'aleph', 'Bet': 'beth', 'Gimel': 'gimel', 'Dalet': 'daleth'}


class TestReplaceVars(TestCase):

    def test_replace_symbols(self):
        for word in SYMBOLS:
            after = '\\' + SYMBOLS[word]
            self.assertEqual(replace_vars('\\[' + word + ']'), after.replace('\\ ', ''))

    def test_replace_infinity(self):
        self.assertEqual(replace_vars('Infinity'), '\\infty')

    def test_none(self):
        self.assertEqual(replace_vars('novariables'), 'novariables')
