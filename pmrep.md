---
title: "\\vspace{-5.6cm}**Portfolio Management TAP**"
author: "\\vspace{-5.5cm}**Sahil Singh**"
header-includes:
   - \usepackage{fancyvrb}
   - \usepackage{amsmath,amssymb,amsthm}
   - \usepackage{environ}
   - \usepackage{verbatim}
   - \usepackage[backend=biber]{biblatex}
   - \usepackage{booktabs}
   - \addbibresource{ref.bib}
output:
    pdf_document
---
**Candidate Number**:243655

# 1. 

The risk-averse investor with utility function $u(x)$ has $u'(x)>0$ meaning investor prefers greater wealth to lesser wealth and $u'(x)<0$ meaning the investor's marginal utility diminishes with increasing risk. According to the First Order Stochastic rule, a distribution F first order stochastically dominates G if for everyx $F(x) < G(x)$. This condition implies that the probability of earning more than x is greater under F than under G.  A rational investor would therefore chose an investment option with distribution F over G.

A distribution F second order stochastically dominates G if for every x $\int_{-\infty}^{x} F(y)dy <\int_{-\infty}^{x} G(y)dy$ . It also implies that $u(x)dF(x)>u(x)dG(x)$. Since this is only true when $u''(x)<0$, it implies that the risk-averse investor would choose the investment option F over G.

Mean Variance Criterion  chooses an investment option F if F has greater mean than G and F has lesser variance than G.

1. If a risk-averse investor is equipped with a utility function $U(R) = a+bR+cR^2$, then $U'(R) = b+2cR$ and $U''(R)=2c$. Since this is a utility function for a risk-averse investor, we need to have $U'(R)>0$ which gives $b+2cR>0$ and $U''(R)<0$ which gives $2c<0$.It gives $b<0$.If these conditions are satisfied, then we can build an appropriate utility function for a risk averse investor. If we further analyse the utility function in terms of expectation, we get $E(U(R)) = a + bE(R) + cE(R^2)+c\sigma_{R}^{2}$, Analysing this further, we get 
$$\frac{\delta E(U(R))}{\delta E(R)} = b + 2cE(R) > 0$$
and 
$$\frac{\delta E(U(R))}{\delta \sigma_{R}^2} = c < 0$$

This implies that utility is increasing with increasing mean and decreasing with increasing variance which is  in accordance to the mean variance criterion.

2. When the returns are mormally distributed, it holds that for distribution F and G  $\int_{-infty}^{x} F(y) dy < \int_{-infty}^{x} G(y) dy$, implies that $E_{F}(R)>E_{F}(R)$ and $V_{F}(R) < V_{G}(R)$ , which is also a criteria for domination of F over G under mean variance criteria. Therefore MVC is an efficient criteria under this condition.


# 2.
 
The single index model returns will be estimated by first calculating beta and alpha for each asset and then using these values to obtain the joint covariance matrix and the means of all assets given and the index.The portfolio obtained had annual mean of 60.93% and annual volatility of 24.71%, while the sharpe ratio obtained wass 2.38. 

# 3.

For investment under uncertainity, the investor can be either risk-averse, risk-lover or risk neutral. If the investor is risk-averse, as is generally the case, then investors utility function  is concave , therefore the investor can borrow at any available rate and form a portfolio that's tangent to the efficient frontier curve. This portfolio can be formed by borrowing  at any risk-free rate.Hence, the so called tangent portfolio can be formed by borrowing at any rate,assuming its available, and therefore does not impact investing decision in uncertain investment options.

For investment under ceratinity, one has to decide between todays and futures consumption. An indifference curve is a curve that includes all points which are the possible combinations of todays and future consumptions with which the investor is satisfied.

The money market line is implemented to add the assumption that th einvestor can borrow or lend at risk free rate. in the financial market.

When we extend the money market line further to the horizontal axis,it provides the maximum consumption that is attainable in the first period.Ann investor can choose to consume less in the current periodd and lend the remaining amount to achieve better consumption in the next period or an investor can choose to consume more today that will drive down future consumption. Thus there is a seperation between financial and investment choices.

# 4. 
We use Black-Litterman model to calculate the posterior mean and posterior covariance from the priors we have.

The updated matrices can  be used to calculate weights for the new portfolio.

The calculationos are performed in the notebook attached.
