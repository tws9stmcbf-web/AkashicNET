"""Focused arithmetic, distribution and boundary checks on synthetic-only methods."""
import itertools
import unittest
import numpy as np
from scipy import stats
import assessment as a

class AssessmentChecks(unittest.TestCase):
    def test_uniform_random_effect_moments(self):
        rng=np.random.default_rng(91)
        s,c=a.latent_rates(rng,(400000,),.30,.25,.05,'shared')
        self.assertAlmostEqual(s.mean(),.30,delta=.0005)
        self.assertAlmostEqual(s.var()/(.30*.70),.05,delta=.0003)
        self.assertAlmostEqual(c.var()/(.25*.75),.05,delta=.0003)
        self.assertAlmostEqual(np.corrcoef(s,c)[0,1],1,places=12)

    def test_independent_pair_components(self):
        s,c=a.latent_rates(np.random.default_rng(9),(100000,),.30,.25,.05,'independent')
        self.assertLess(abs(np.corrcoef(s,c)[0,1]),.012)

    def test_t_matches_scipy(self):
        x=np.array([[.01,.04,-.02,.03],[.04,.08,.01,-.02]])
        np.testing.assert_allclose(a.t_pvalue(x),stats.ttest_1samp(x,0,axis=1,alternative='greater').pvalue)

    def test_degenerate_no_rejection(self):
        np.testing.assert_equal(a.t_pvalue(np.array([[.1,.1,.1],[0,0,0]])),[1,1])

    def test_conditional_shuffle_against_enumeration(self):
        t=np.array([0,0,1,3]); r=np.array([0,0,0,3]); e=np.ones(4,dtype=bool)
        assignments=set(itertools.permutations(t))
        exact=np.array([np.count_nonzero(np.array(z)==r) for z in assignments])
        draws=a.conditional_hits(np.random.default_rng(6),[t],[r],[e],100000)
        self.assertAlmostEqual(draws.mean(),exact.mean(),delta=.012)
        self.assertAlmostEqual((draws>=3).mean(),.25,delta=.006)
        for k in range(5): self.assertAlmostEqual((draws==k).mean(),(exact==k).mean(),delta=.006)

    def test_ineligible_rows_kept_in_target_support(self):
        t=np.array([0,0,1,3]); r=np.array([0,0,0,3]); e=np.array([1,0,1,0],dtype=bool)
        draws=a.conditional_hits(np.random.default_rng(6),[t],[r],[e],100000)
        # Two eligible up responses, with 2 of 4 targets up: expected hits=1.
        self.assertAlmostEqual(draws.mean(),1,delta=.01)

    def test_constant_response_shuffle_is_degenerate(self):
        t=np.array([0,1,2,3]);r=np.zeros(4,dtype=int);e=np.ones(4,dtype=bool)
        np.testing.assert_equal(a.conditional_hits(np.random.default_rng(8),[t],[r],[e],100),np.ones(100))

    def test_condition_hypergeometric_matches_enumeration(self):
        h=np.array([1,1,0,0]);dist=[]
        for c in itertools.combinations(range(4),2):dist.append(h[list(c)].sum())
        exact=np.bincount(dist,minlength=3)/len(dist)
        np.testing.assert_allclose(stats.hypergeom.pmf([0,1,2],4,2,2),exact)

    def test_plus_one_and_ties(self):
        rng=np.random.default_rng(2)
        t=np.zeros((2,2,4),dtype=int); r=np.zeros_like(t); e=np.ones_like(t,dtype=bool)
        c=np.zeros_like(e);c[:,:,:2]=True
        pt,pd,pr,ex,hs,hc=a.randomization_pvalues(rng,t,r,c,e,99)
        self.assertEqual(pt,1);self.assertEqual(pd,1);self.assertGreaterEqual(pr,.01)
        self.assertEqual(ex,8);self.assertEqual(hs,8);self.assertEqual(hc,8)

    def test_summary_reproducible_and_omission_gate(self):
        args=(500,30,100,.30,.25,.05,'independent','differential')
        x=a.summary_run(np.random.default_rng(23),*args)
        y=a.summary_run(np.random.default_rng(23),*args)
        self.assertEqual(x,y)
        self.assertLess(x['gate_pass'],.01)

    def test_response_blind_null_not_information_injection(self):
        # Strong biased serial guesses must retain .25 unconditional match chance.
        rng=np.random.default_rng(109)
        vals=[]
        for _ in range(200):
            t,y,c,e=a.trial_data(rng,30,40,.25,.25,0,'independent')
            vals.append(np.mean(t==y))
        self.assertAlmostEqual(np.mean(vals),.25,delta=.004)

    def test_invalid_rates_rejected(self):
        with self.assertRaises(ValueError):a.latent_rates(np.random.default_rng(1),(1000,),.02,.25,.5,'independent')

if __name__=='__main__':unittest.main()
