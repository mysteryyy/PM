---
title: "\\vspace{-5.6cm}**PM Notes**"
bibliography: pm.bib
header-includes:
   - \usepackage{fancyvrb}
   - \usepackage{amsmath,amssymb,amsthm}
   - \usepackage{environ}
   - \usepackage{verbatim}
   - \usepackage[backend=biber]{biblatex}
   - \addbibresource{pm.bib}
output:
    pdf_document
---

portfolio-2.pdf = Modern Portfolio Theory and Investment Analysis

# To Do

Compare simple beta estimation results with bayesian analysis results.

# Notes

1. Chapter 7 of portfolio-2.pdf for adjusted betas, beta should be adjusted using bayesian technique mentioned.

2. Page 161 of portfolio-2.pdf single index model outperforms multi-index models @jointsingind.

3. Pg 165(portfolio-2.pdf) 1st para fama french test on forecasting future correlation model(@chan1999portfolio). Constant correlaation outperforms single index and fama french in forecasting correlations.

4. Measuring Performance using benchmark with modified sharpe portolfio-2.pdf Pg 678

5. Recently @jagannathan2003risk, proved
that mean-variance optimizers are already implicitly applying some form of shrinkage to
the sample covariance matrix when short sales are ruled out, and that this is generally
beneficial in terms of improving weights stability


6.  @allen2019defense says,


> The theory that high-frequency data can be used to eliminate estimation error in the covariance matrix is constrained in practice because of microstructure issues, thin trading, and departures from normality, all of which place a limit on precision (@hansen2006realized). As a result, lower-frequency data tend to be used in conjunction with factor models to estimate the covariance matrix for investment problems involving large numbers of assets. 

7. @allen2019defense says 

> Our results cast doubt on the conclusion of
> DeMiguel et al. (2009) that mean–variance is
> unworkable in higher dimensions. Consider that
> Grinold and Kahn (1999) developed a simple binary
> model that relates the information coefficient to the
> number of forecasts that are directionally correct
> (the “hit rate”). Our IC of 0.07 equates to a hit rate
> of just 53.5% a month, or an R2 of 0.5%. That such
> modest levels of forecasting ability can generate
> meaningful gains in utility is remarkable. The uplift
> in utility is tangible, and it is a benefit that increases
> with the size of the asset universe.

8. According to @ehsani2022factor, 

> Factor momentum’s ability to span individual stock momentum, but not vice versa, suggests
> that individual stock momentum is a manifestation of factor momentum. An investor who trades
> individual stock momentum indirectly times factors, and an investor who directly times factors
> performs better. The indirect method loses out because it also takes positions based on noise. The
> other possible sources of momentum profits do not contribute to these profits, and so their inclusion
> renders the strategy unnecessarily volatile.

Basically saying that stock momentum is a result of factor momentum.

# References
