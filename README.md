[![Build Status](https://travis-ci.org/weibullguy/rtk.svg?branch=master)](https://travis-ci.org/weibullguy/rtk)
[![Build Status](https://travis-ci.org/weibullguy/rtk.svg?branch=develop)](https://travis-ci.org/weibullguy/rtk)

# rtk
Reliability, Availability, Maintainability, Safety (RAMS) analysis program.

RTK is an open-source application similar to PTC's Windchill Quality or the
Reliasoft line of products. The Reliability ToolKit (RTK) currently has modules
for:

* Function Module
    * Functional decomposition
    * Functional FMEA
    * Reliability analysis of system functions
    * Hardware/Function matrix
    * Software/Function matrix
    * Development Testing/Function matrix
* Requirements Module
    * Stakeholder input prioritization
    * Requirement development
    * Analysis of requirement for clarity, completeness, consistency, and
      verifiability
* Hardware Module
    * Reliability allocation
        * Equal apportionment
        * AGREE apportionment
        * ARINC apportionment
        * Feasibility of Objectives
    * Hazards analysis
    * Hardware reliability predictions using various methods
        * Similar items analysis
        * MIL-HDBK-217FN2 parts count
        * MIL-HDBK-217FN2 parts stress
    * FMEA/FMECA
        * RPN
        * MIL-STD-1629A, Task 102
    * Physics of failure analysis
* Software Module
    * Risk analysis
    * Test planning
    * Reliability estimation
* Test Module
    * Reliability growth
        * Planning
        * Feasibility
        * Assessment
    * HALT/HASS (planned)
    * ALT (planned)
    * ESS (planned)
    * Reliability Demonstration (planned)
    * PRAT (planned)
* Validation Module
    * Task description
    * Task acceptance value(s)
    * Task time
    * Task cost
    * Overall validation plan time/cost estimates
* Incidents Module
    * Incident description
    * Incident chargeability
    * Incident analysis
    * Corrective action
* Survival Analysis Module
    * Non-Parametric Methods
        * Kaplan-Meier (product limit)
        * Mean Cumulative Function (MCF)
    * Parametric Methods
        * NHPP - Power Law
        * NHPP - LogLinear
        * Exponential
        * LogNormal
        * Normal
        * Weibull
        * WeiBayes (planned)
    * Fitting Methods
        * Maximum Likelihood Estimates
        * Regression
    * One- and two-side confidence bounds
        * Crow (NHPP only)
        * Duane (NHPP only)
        * Fisher Matrix
        * Likelihood
        * Bootstrap (planned)

