
__author__ = 'Kevin Chen'
__status__ = 'Development'

from unittest import TestCase
from MathematicaToLaTeX import beta
from MathematicaToLaTeX import cfk
from MathematicaToLaTeX import gamma
from MathematicaToLaTeX import integrate
from MathematicaToLaTeX import legendrep
from MathematicaToLaTeX import legendreq
from MathematicaToLaTeX import polyeulergamma
from MathematicaToLaTeX import product
from MathematicaToLaTeX import qpochhammer
from MathematicaToLaTeX import summation


class TestBeta(TestCase):

    def test_single(self):
        self.assertEqual(beta('Beta[a,b]'), '\\EulerBeta@{a}{b}')
        self.assertEqual(beta('--Beta[a,b]--'), '--\\EulerBeta@{a}{b}--')
        self.assertEqual(beta('Beta[z,a,b]'), '\\IncBeta{z}@{a}{b}')
        self.assertEqual(beta('--Beta[z,a,b]--'), '--\\IncBeta{z}@{a}{b}--')
        self.assertEqual(beta('Beta[a,b]Beta[z,a,b]'), '\\EulerBeta@{a}{b}\\IncBeta{z}@{a}{b}')
        self.assertEqual(beta('--Beta[a,b]--Beta[z,a,b]--'), '--\\EulerBeta@{a}{b}--\\IncBeta{z}@{a}{b}--')

    def test_nested(self):
        self.assertEqual(beta('Beta[Beta[a,b],Beta[a,b]]'), '\\EulerBeta@{\\EulerBeta@{a}{b}}{\\EulerBeta@{a}{b}}')
        self.assertEqual(beta('--Beta[Beta[a,b],Beta[a,b]]--'), '--\\EulerBeta@{\\EulerBeta@{a}{b}}{\\EulerBeta@{a}{b}}--')
        self.assertEqual(beta('Beta[Beta[z,a,b],Beta[z,a,b],Beta[z,a,b]]'), '\\IncBeta{\\IncBeta{z}@{a}{b}}@{\\IncBeta{z}@{a}{b}}{\\IncBeta{z}@{a}{b}}')
        self.assertEqual(beta('--Beta[Beta[z,a,b],Beta[z,a,b],Beta[z,a,b]]--'), '--\\IncBeta{\\IncBeta{z}@{a}{b}}@{\\IncBeta{z}@{a}{b}}{\\IncBeta{z}@{a}{b}}--')

    def test_exceptions(self):
        self.assertEqual(beta('BetaRegularized[z,a,b]'), 'BetaRegularized[z,a,b]')
        self.assertEqual(beta('\\[Beta]'), '\\[Beta]')

    def test_none(self):
        self.assertEqual(beta('none'), 'none')


class TestCFK(TestCase):

    def test_none(self):
        self.assertEqual(cfk('none'), 'none')


class TestGamma(TestCase):

    def test_none(self):
        self.assertEqual(gamma('none'), 'none')


class TestIntegrate(TestCase):

    def test_none(self):
        self.assertEqual(integrate('none'), 'none')


class TestLegendreP(TestCase):

    def test_none(self):
        self.assertEqual(legendrep('none'), 'none')


class TestLegendreQ(TestCase):

    def test_none(self):
        self.assertEqual(legendreq('none'), 'none')


class TestPolyEulergamma(TestCase):

    def test_none(self):
        self.assertEqual(polyeulergamma('none'), 'none')


class TestProduct(TestCase):

    def test_none(self):
        self.assertEqual(product('none'), 'none')


class TestQPochhammer(TestCase):

    def test_none(self):
        self.assertEqual(qpochhammer('none'), 'none')


class TestSummation(TestCase):

    def test_none(self):
        self.assertEqual(summation('none'), 'none')