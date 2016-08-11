
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

    def test_single(self):
        self.assertEqual(cfk('ContinuedFractionK[f,g,{i,imin,imax}]'), '\\CFK{i}{imin}{imax}@@{f}{g}')
        self.assertEqual(cfk('--ContinuedFractionK[f,g,{i,imin,imax}]--'), '--\\CFK{i}{imin}{imax}@@{f}{g}--')
        self.assertEqual(cfk('ContinuedFractionK[g,{i,imin,imax}]'), '\\CFK{i}{imin}{imax}@@{1}{g}')
        self.assertEqual(cfk('--ContinuedFractionK[g,{i,imin,imax}]--'), '--\\CFK{i}{imin}{imax}@@{1}{g}--')
        self.assertEqual(cfk('ContinuedFractionK[f,g,{i,imin,imax}]ContinuedFractionK[g,{i,imin,imax}]'), '\\CFK{i}{imin}{imax}@@{f}{g}\\CFK{i}{imin}{imax}@@{1}{g}')
        self.assertEqual(cfk('--ContinuedFractionK[f,g,{i,imin,imax}]--ContinuedFractionK[g,{i,imin,imax}]--'), '--\\CFK{i}{imin}{imax}@@{f}{g}--\\CFK{i}{imin}{imax}@@{1}{g}--')

    def test_nested(self):
        self.assertEqual(cfk('ContinuedFractionK[ContinuedFractionK[f,g,{i,imin,imax}],ContinuedFractionK[f,g,{i,imin,imax}],{i,imin,imax}]'), '\\CFK{i}{imin}{imax}@@{\\CFK{i}{imin}{imax}@@{f}{g}}{\\CFK{i}{imin}{imax}@@{f}{g}}')
        self.assertEqual(cfk('--ContinuedFractionK[ContinuedFractionK[f,g,{i,imin,imax}],ContinuedFractionK[f,g,{i,imin,imax}],{i,imin,imax}]--'), '--\\CFK{i}{imin}{imax}@@{\\CFK{i}{imin}{imax}@@{f}{g}}{\\CFK{i}{imin}{imax}@@{f}{g}}--')
        self.assertEqual(cfk('ContinuedFractionK[ContinuedFractionK[g,{i,imin,imax}],{i,imin,imax}]'), '\\CFK{i}{imin}{imax}@@{1}{\\CFK{i}{imin}{imax}@@{1}{g}}')

    def test_none(self):
        self.assertEqual(cfk('none'), 'none')


class TestGamma(TestCase):

    def test_single(self):
        self.assertEqual(gamma('Gamma[z]'), '\\EulerGamma@{z}')
        self.assertEqual(gamma('--Gamma[z]--'), '--\\EulerGamma@{z}--')
        self.assertEqual(gamma('Gamma[a,z]'), '\\IncGamma@{a}{z}')
        self.assertEqual(gamma('--Gamma[a,z]--'), '--\\IncGamma@{a}{z}--')
        self.assertEqual(gamma('Gamma[a,z0,z1]'), '\\IncGamma@{a}{z0} - \\IncGamma@{a}{z1}')
        self.assertEqual(gamma('--Gamma[a,z0,z1]--'), '--\\IncGamma@{a}{z0} - \\IncGamma@{a}{z1}--')

    def test_nested(self):
        self.assertEqual(gamma('Gamma[Gamma[z]]'), '\\EulerGamma@{\\EulerGamma@{z}}')
        self.assertEqual(gamma('--Gamma[Gamma[z]]--'), '--\\EulerGamma@{\\EulerGamma@{z}}--')
        self.assertEqual(gamma('Gamma[Gamma[a,z],Gamma[a,z]]'), '\\IncGamma@{\\IncGamma@{a}{z}}{\\IncGamma@{a}{z}}')
        self.assertEqual(gamma('--Gamma[Gamma[a,z],Gamma[a,z]]--'), '--\\IncGamma@{\\IncGamma@{a}{z}}{\\IncGamma@{a}{z}}--')

    def test_exceptions(self):
        self.assertEqual(gamma('PolyGamma[n,z]'), 'PolyGamma[n,z]')
        self.assertEqual(gamma('\\[CapitalGamma]'), '\\[CapitalGamma]')
        self.assertEqual(gamma('LogGamma[z]'), 'LogGamma[z]')
        self.assertEqual(gamma('EulerGamma'), 'EulerGamma')
        self.assertEqual(gamma('\\IncGamma@{a}{b}'), '\\IncGamma@{a}{b}')
        self.assertEqual(gamma('\\[Gamma]'), '\\[Gamma]')
        self.assertEqual(gamma('\\GammaQ@{a}{z}'), '\\GammaQ@{a}{z}')
        self.assertEqual(gamma('GammaRegularized[a,z]'), 'GammaRegularized[a,z]')
        self.assertEqual(gamma('StieltjesGamma[k]'), 'StieltjesGamma[k]')

    def test_none(self):
        self.assertEqual(gamma('none'), 'none')


class TestIntegrate(TestCase):

    def test_single(self):
        self.assertEqual(integrate('Integrate[f,{x,xmin,xmax}]'), '\\int_{xmin}^{xmax}{f}d{x}')
        self.assertEqual(integrate('--Integrate[f,{x,xmin,xmax}]--'), '--\\int_{xmin}^{xmax}{f}d{x}--')

    def test_nested(self):
        self.assertEqual(integrate('Integrate[Integrate[f,{x,xmin,xmax}],{Integrate[f,{x,xmin,xmax}],xmin,xmax}]'), '\\int_{xmin}^{xmax}{\\int_{xmin}^{xmax}{f}d{x}}d{\\int_{xmin}^{xmax}{f}d{x}}')
        self.assertEqual(integrate('--Integrate[Integrate[f,{x,xmin,xmax}],{Integrate[f,{x,xmin,xmax}],xmin,xmax}]--'), '--\\int_{xmin}^{xmax}{\\int_{xmin}^{xmax}{f}d{x}}d{\\int_{xmin}^{xmax}{f}d{x}}--')

    def test_none(self):
        self.assertEqual(integrate('none'), 'none')


class TestLegendreP(TestCase):

    def test_single(self):
        self.assertEqual(legendrep('LegendreP[n,x]'), '\\LegendreP{n}@{x}')
        self.assertEqual(legendrep('--LegendreP[n,x]--'), '--\\LegendreP{n}@{x}--')
        self.assertEqual(legendrep('LegendreP[n,m,1,x]'), '\\FerrersP[m]{n}@{x}')
        self.assertEqual(legendrep('--LegendreP[n,m,1,x]--'), '--\\FerrersP[m]{n}@{x}--')
        self.assertEqual(legendrep('LegendreP[n,m,2,x]'), '\\FerrersP[m]{n}@{x}')
        self.assertEqual(legendrep('--LegendreP[n,m,2,x]--'), '--\\FerrersP[m]{n}@{x}--')
        self.assertEqual(legendrep('LegendreP[n,m,3,x]'), '\\LegendreP[m]{n}@{x}')
        self.assertEqual(legendrep('--LegendreP[n,m,3,x]--'), '--\\LegendreP[m]{n}@{x}--')

    def test_nested(self):
        self.assertEqual(legendrep('LegendreP[LegendreP[n,x],LegendreP[n,x]]'), '\\LegendreP{\\LegendreP{n}@{x}}@{\\LegendreP{n}@{x}}')
        self.assertEqual(legendrep('--LegendreP[LegendreP[n,x],LegendreP[n,x]]--'), '--\\LegendreP{\\LegendreP{n}@{x}}@{\\LegendreP{n}@{x}}--')
        self.assertEqual(legendrep('LegendreP[LegendreP[n,m,1,x],LegendreP[n,m,1,x],1,LegendreP[n,m,1,x]]'), '\\FerrersP[\\FerrersP[m]{n}@{x}]{\\FerrersP[m]{n}@{x}}@{\\FerrersP[m]{n}@{x}}')
        self.assertEqual(legendrep('--LegendreP[LegendreP[n,m,1,x],LegendreP[n,m,1,x],1,LegendreP[n,m,1,x]]--'), '--\\FerrersP[\\FerrersP[m]{n}@{x}]{\\FerrersP[m]{n}@{x}}@{\\FerrersP[m]{n}@{x}}--')
        self.assertEqual(legendrep('LegendreP[LegendreP[n,m,3,x],LegendreP[n,m,3,x],3,LegendreP[n,m,3,x]]'), '\\LegendreP[\\LegendreP[m]{n}@{x}]{\\LegendreP[m]{n}@{x}}@{\\LegendreP[m]{n}@{x}}')
        self.assertEqual(legendrep('--LegendreP[LegendreP[n,m,3,x],LegendreP[n,m,3,x],3,LegendreP[n,m,3,x]]--'), '--\\LegendreP[\\LegendreP[m]{n}@{x}]{\\LegendreP[m]{n}@{x}}@{\\LegendreP[m]{n}@{x}}--')

    def test_none(self):
        self.assertEqual(legendrep('none'), 'none')


class TestLegendreQ(TestCase):

    def test_single(self):
        self.assertEqual(legendreq('LegendreQ[n,x]'), '\\LegendreQ{n}@{x}')
        self.assertEqual(legendreq('--LegendreQ[n,x]--'), '--\\LegendreQ{n}@{x}--')
        self.assertEqual(legendreq('LegendreQ[n,m,1,x]'), '\\FerrersQ[m]{n}@{x}')
        self.assertEqual(legendreq('--LegendreQ[n,m,1,x]--'), '--\\FerrersQ[m]{n}@{x}--')
        self.assertEqual(legendreq('LegendreQ[n,m,2,x]'), '\\FerrersQ[m]{n}@{x}')
        self.assertEqual(legendreq('--LegendreQ[n,m,2,x]--'), '--\\FerrersQ[m]{n}@{x}--')
        self.assertEqual(legendreq('LegendreQ[n,m,3,x]'), '\\LegendreQ[m]{n}@{x}')
        self.assertEqual(legendreq('--LegendreQ[n,m,3,x]--'), '--\\LegendreQ[m]{n}@{x}--')

    def test_nested(self):
        self.assertEqual(legendreq('LegendreQ[LegendreQ[n,x],LegendreQ[n,x]]'), '\\LegendreQ{\\LegendreQ{n}@{x}}@{\\LegendreQ{n}@{x}}')
        self.assertEqual(legendreq('--LegendreQ[LegendreQ[n,x],LegendreQ[n,x]]--'), '--\\LegendreQ{\\LegendreQ{n}@{x}}@{\\LegendreQ{n}@{x}}--')
        self.assertEqual(legendreq('LegendreQ[LegendreQ[n,m,1,x],LegendreQ[n,m,1,x],1,LegendreQ[n,m,1,x]]'), '\\FerrersQ[\\FerrersQ[m]{n}@{x}]{\\FerrersQ[m]{n}@{x}}@{\\FerrersQ[m]{n}@{x}}')
        self.assertEqual(legendreq('--LegendreQ[LegendreQ[n,m,1,x],LegendreQ[n,m,1,x],1,LegendreQ[n,m,1,x]]--'), '--\\FerrersQ[\\FerrersQ[m]{n}@{x}]{\\FerrersQ[m]{n}@{x}}@{\\FerrersQ[m]{n}@{x}}--')
        self.assertEqual(legendreq('LegendreQ[LegendreQ[n,m,3,x],LegendreQ[n,m,3,x],3,LegendreQ[n,m,3,x]]'), '\\LegendreQ[\\LegendreQ[m]{n}@{x}]{\\LegendreQ[m]{n}@{x}}@{\\LegendreQ[m]{n}@{x}}')
        self.assertEqual(legendreq('--LegendreQ[LegendreQ[n,m,3,x],LegendreQ[n,m,3,x],3,LegendreQ[n,m,3,x]]--'), '--\\LegendreQ[\\LegendreQ[m]{n}@{x}]{\\LegendreQ[m]{n}@{x}}@{\\LegendreQ[m]{n}@{x}}--')

    def test_none(self):
        self.assertEqual(legendreq('none'), 'none')


class TestPolyEulergamma(TestCase):

    def test_single(self):
        self.assertEqual(polyeulergamma('PolyGamma[z]'), '\\digamma@{z}')
        self.assertEqual(polyeulergamma('--PolyGamma[z]--'), '--\\digamma@{z}--')
        self.assertEqual(polyeulergamma('PolyGamma[n,z]'), '\\polygamma{n}@{z}')
        self.assertEqual(polyeulergamma('--PolyGamma[n,z]--'), '--\\polygamma{n}@{z}--')
        self.assertEqual(polyeulergamma('PolyGamma[z]PolyGamma[n,z]'), '\\digamma@{z}\\polygamma{n}@{z}')
        self.assertEqual(polyeulergamma('--PolyGamma[z]--PolyGamma[n,z]--'), '--\\digamma@{z}--\\polygamma{n}@{z}--')

    def test_nested(self):
        self.assertEqual(polyeulergamma('PolyGamma[PolyGamma[z]]'), '\\digamma@{\\digamma@{z}}')
        self.assertEqual(polyeulergamma('--PolyGamma[PolyGamma[z]]--'), '--\\digamma@{\\digamma@{z}}--')
        self.assertEqual(polyeulergamma('PolyGamma[PolyGamma[n,z],PolyGamma[n,z]]'), '\\polygamma{\\polygamma{n}@{z}}@{\\polygamma{n}@{z}}')
        self.assertEqual(polyeulergamma('--PolyGamma[PolyGamma[n,z],PolyGamma[n,z]]--'), '--\\polygamma{\\polygamma{n}@{z}}@{\\polygamma{n}@{z}}--')

    def test_none(self):
        self.assertEqual(polyeulergamma('none'), 'none')


class TestProduct(TestCase):

    def test_single(self):
        self.assertEqual(product('Product[f,{i,imin,imax}]'), '\\Prod{i}{imin}{imax}@{f}')
        self.assertEqual(product('--Product[f,{i,imin,imax}]--'), '--\\Prod{i}{imin}{imax}@{f}--')

    def test_nested(self):
        self.assertEqual(product('Product[Product[f,{i,imin,imax}],{Product[f,{i,imin,imax}],imin,imax}]'), '\\Prod{\\Prod{i}{imin}{imax}@{f}}{imin}{imax}@{\\Prod{i}{imin}{imax}@{f}}')
        self.assertEqual(product('--Product[Product[f,{i,imin,imax}],{Product[f,{i,imin,imax}],imin,imax}]--'), '--\\Prod{\\Prod{i}{imin}{imax}@{f}}{imin}{imax}@{\\Prod{i}{imin}{imax}@{f}}--')

    def test_none(self):
        self.assertEqual(product('none'), 'none')


class TestQPochhammer(TestCase):

    def test_single(self):
        self.assertEqual(qpochhammer('QPochhammer[a,q,n]'), '\\qPochhammer{a}{q}{n}')
        self.assertEqual(qpochhammer('--QPochhammer[a,q,n]--'), '--\\qPochhammer{a}{q}{n}--')
        self.assertEqual(qpochhammer('QPochhammer[a,q]'), '\\qPochhammer{a}{q}{\\infty}')
        self.assertEqual(qpochhammer('--QPochhammer[a,q]--'), '--\\qPochhammer{a}{q}{\\infty}--')
        self.assertEqual(qpochhammer('QPochhammer[q]'), '\\qPochhammer{q}{q}{\\infty}')
        self.assertEqual(qpochhammer('--QPochhammer[q]--'), '--\\qPochhammer{q}{q}{\\infty}--')
        self.assertEqual(qpochhammer('QPochhammer[a,q,n]QPochhammer[a,q]QPochhammer[q]'), '\\qPochhammer{a}{q}{n}\\qPochhammer{a}{q}{\\infty}\\qPochhammer{q}{q}{\\infty}')
        self.assertEqual(qpochhammer('--QPochhammer[a,q,n]--QPochhammer[a,q]--QPochhammer[q]--'), '--\\qPochhammer{a}{q}{n}--\\qPochhammer{a}{q}{\\infty}--\\qPochhammer{q}{q}{\\infty}--')

    def test_nested(self):
        self.assertEqual(qpochhammer('QPochhammer[QPochhammer[q],QPochhammer[q],QPochhammer[q]]'), '\\qPochhammer{\\qPochhammer{q}{q}{\\infty}}{\\qPochhammer{q}{q}{\\infty}}{\\qPochhammer{q}{q}{\\infty}}')
        self.assertEqual(qpochhammer('--QPochhammer[QPochhammer[q],QPochhammer[q],QPochhammer[q]]--'), '--\\qPochhammer{\\qPochhammer{q}{q}{\\infty}}{\\qPochhammer{q}{q}{\\infty}}{\\qPochhammer{q}{q}{\\infty}}--')
        self.assertEqual(qpochhammer('QPochhammer[QPochhammer[q],QPochhammer[q]]'), '\\qPochhammer{\\qPochhammer{q}{q}{\\infty}}{\\qPochhammer{q}{q}{\\infty}}{\\infty}')
        self.assertEqual(qpochhammer('--QPochhammer[QPochhammer[q],QPochhammer[q]]--'), '--\\qPochhammer{\\qPochhammer{q}{q}{\\infty}}{\\qPochhammer{q}{q}{\\infty}}{\\infty}--')

    def test_none(self):
        self.assertEqual(qpochhammer('none'), 'none')


class TestSummation(TestCase):

    def test_single(self):
        self.assertEqual(summation('Sum[f,{i,imin,imax}]'), '\\Sum{i}{imin}{imax}@{f}')
        self.assertEqual(summation('--Sum[f,{i,imin,imax}]--'), '--\\Sum{i}{imin}{imax}@{f}--')

    def test_nested(self):
        self.assertEqual(summation('Sum[Sum[f,{i,imin,imax}],{Sum[f,{i,imin,imax}],imin,imax}]'), '\\Sum{\\Sum{i}{imin}{imax}@{f}}{imin}{imax}@{\\Sum{i}{imin}{imax}@{f}}')
        self.assertEqual(summation('--Sum[Sum[f,{i,imin,imax}],{Sum[f,{i,imin,imax}],imin,imax}]--'), '--\\Sum{\\Sum{i}{imin}{imax}@{f}}{imin}{imax}@{\\Sum{i}{imin}{imax}@{f}}--')

    def test_none(self):
        self.assertEqual(summation('none'), 'none')