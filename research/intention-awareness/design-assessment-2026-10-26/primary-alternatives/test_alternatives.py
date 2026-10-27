"""Independent analytic/enumeration checks, not scientific validation."""
import itertools
import unittest

import numpy as np
from scipy import stats
import alternatives as a


class MethodChecks(unittest.TestCase):
    def test_e_factor_expectation_and_exact_tail(self):
        # Enumerate all sufficient binomial counts for bounded two-point nulls.
        for n in [3,20,60]:
            for p in [.02,.1,.5,.9]:
                low=-p;high=1-p
                rows=np.array([[high]*k+[low]*(n-k) for k in range(n+1)])
                probs=stats.binom.pmf(np.arange(n+1),n,p)
                loge=a.betting_log_e(rows,0,-1,1)
                self.assertLessEqual(np.dot(probs,np.exp(loge)),1+1e-12)
                self.assertLessEqual(probs[loge>=np.log(20)].sum(),.05+1e-12)

    def test_betting_is_fixed_mixture_not_maximum(self):
        x=np.array([[.1,.2,-.3,.4],[.9,-.8,.7,.6]])
        capitals=np.array([np.prod(1+l*x,axis=1) for l in a.FRACTIONS])
        np.testing.assert_allclose(np.exp(a.betting_log_e(x,0,-1,1)),capitals.mean(axis=0))
        np.testing.assert_allclose(a.betting_log_e(x[:,::-1],0,-1,1),a.betting_log_e(x,0,-1,1))

    def test_bounds_do_not_use_observed_minimum(self):
        x=np.ones((1,20))*.02
        # A tiny observed range must not allow a large bet or empirical-bound rejection.
        self.assertLess(a.betting_log_e(x,0,-1,1)[0],np.log(20))
        self.assertLess(a.bernstein_lower(x,-1,1)[0],0)
        with self.assertRaises(ValueError): a.betting_log_e(np.array([[1.01,0.]]),.25,0,1)
        with self.assertRaises(ValueError): a.betting_log_e(np.array([[np.nan,0.]]),.25,0,1)

    def test_bernstein_formula_and_rescaling(self):
        x=np.array([[0.,.1,.8,.9,.5]])
        log=np.log(40)
        expected=x.mean(axis=1)-np.sqrt(2*x.var(axis=1,ddof=1)*log/5)-7*log/12
        np.testing.assert_allclose(a.bernstein_lower(x,0,1),expected)
        np.testing.assert_allclose(a.bernstein_lower(2*x-1,-1,1),2*expected-1)

    def test_bernstein_exact_binomial_tail(self):
        n=60
        rows=np.array([[1.]*k+[0.]*(n-k) for k in range(n+1)])
        lb=a.bernstein_lower(rows,0,1)
        for p in [.02,.1,.25,.5,.9]:
            size=stats.binom.pmf(np.arange(n+1),n,p)[lb>p].sum()
            self.assertLessEqual(size,.05+1e-12)

    def test_hoeffding_agrees_with_inherited_contrast_bound(self):
        x=np.array([[.01,.1,-.05,.03]*20,[.4,.5,.3,.4]*20])
        bound=np.exp(-x.shape[1]*np.maximum(x.mean(axis=1),0)**2/2)
        np.testing.assert_array_equal(a.hoeffding_lower(x,-1,1)>0,bound<.05)

    def test_bootstrap_against_exhaustive_resamples(self):
        x=np.array([[[.01,.06,-.03]],[[.02,-.05,.09]]])
        ix=np.array(list(itertools.product(range(3),repeat=3)))[None,:,:]
        got=a.bootstrap_from_indices(x,ix)
        for k in range(2):
            observed=x[k,0].mean()/(x[k,0].std(ddof=1)/np.sqrt(3))
            exceed=0
            for row in ix[0]:
                sample=x[k,0,row]
                se=sample.std(ddof=1)/np.sqrt(3)
                pivot=(sample.mean()-x[k,0].mean())/se if se>1e-14 else np.inf
                exceed+=pivot>=observed-1e-12
            self.assertEqual(got[k][0],(1+exceed)/28)

    def test_degenerate_bootstrap_is_no_rejection(self):
        ix=np.zeros((1,19,3),dtype=int)
        x=np.array([[[.1,.1,.1]],[[0.,0.,0.]]])
        pa,pd=a.bootstrap_from_indices(x,ix)
        self.assertEqual(pa[0],1);self.assertEqual(pd[0],1)

    def test_null_mixture_means_and_negative_covariance(self):
        scenarios={s['id']:s for s in a.PLAN['scenarios']}
        for name in ['delta_skew10','delta_reverse10','delta_rare02','chance_skew10','delta_negative_cov']:
            s,c,g=a.generate(np.random.default_rng(91),3000,160,scenarios[name])
            self.assertAlmostEqual(s.mean()-.25,scenarios[name]['A'],delta=.0006)
            self.assertAlmostEqual((s-c).mean(),scenarios[name]['Delta'],delta=.0007)
            self.assertTrue(g.all())
            if name=='delta_negative_cov': self.assertLess(np.corrcoef(s.ravel(),c.ravel())[0,1],-.75)

    def test_reproducibility_and_both_success_criteria(self):
        scenario=a.PLAN['scenarios'][0]
        x=a.generate(np.random.default_rng(19),30,20,scenario)
        y=a.generate(np.random.default_rng(19),30,20,scenario)
        for xx,yy in zip(x,y): np.testing.assert_array_equal(xx,yy)
        s=np.full((1,160),.22);c=np.zeros((1,160))
        for method,(ra,rd) in a.analytic_flags(s,c).items(): self.assertFalse((ra&rd)[0],method)
        s=np.full((1,160),.4);c=np.full((1,160),.5)
        for method,(ra,rd) in a.analytic_flags(s,c).items(): self.assertFalse((ra&rd)[0],method)

    def test_bootstrap_seed_reproducible(self):
        s=np.array([[.2,.3,.4,.22],[.29,.4,.32,.18]])
        c=np.array([[.3,.2,.3,.18],[.31,.3,.22,.12]])
        x=a.bootstrap_flags(np.random.default_rng(41),s,c,99)
        y=a.bootstrap_flags(np.random.default_rng(41),s,c,99)
        for xx,yy in zip(x,y): np.testing.assert_array_equal(xx,yy)

    def test_omissions_shift_operational_mean_and_fail_gate(self):
        scenario=a.PLAN['scenarios'][-1]
        s,c,g=a.generate(np.random.default_rng(91),3000,160,scenario)
        self.assertAlmostEqual(s.mean(),.294,delta=.0004)
        self.assertAlmostEqual(c.mean(),.180,delta=.0004)
        self.assertLess(g.mean(),.001)


if __name__=='__main__': unittest.main()
