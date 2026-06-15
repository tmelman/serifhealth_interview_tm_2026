# serifhealth_interview_tm_2026

## Overview
In this repo is code for understanding and matching hospital billing data to insurance provider data. There are two datasets:
* hpt_extract_20250213.csv: hospital data containing entries for each procedure type including billing/cost information.
* tic_extract_20250203.csv: payer data containing entries for amount payed for each procedure, hospital, etc.

Included in this repo is src code referenced in the two notebooks. One notebook contains scratchwork for understanding the dataset; the other contains more polished code for matching the two datasets. 

## Discussion on example questions
In terms of the first two example questions, I explored the data to understand the following:
### For UHC code 43239: 
* three rows show up in the hpt dataset. One has the rate 6438 as standard_charge_negotiated_dollar and standard_charge max; the other two rows show lower rates. The first one is for "all payer" plan types; the other two have medicare plan types. All 3 were at Mount Sinai. It's consistent with prior assumptions here that medicare bills lower than private insurance. Those are also on a "fee schedule", so these could be installment values and not total values billed. However I would have expected the TIC table to label these in the "negotiation_type" as "fee schedule" but they are not, so it's difficult to see any relationship there.
* For the tic dataset for the ein associated with mount sinai (131624096), one row has the 6438 rate; the other rows show lower rates. One difference is the institutional vs professional setting: professional settings show lower rates than institutional. 
* There seems no clean way to rate match the other TIC entries; the other HPT rows are fee schedule, and we don't have NPI values in the HPT table on which to match for individual providers/prescribers. We can guess at which of the rows in the TIC match based on which are lower than the negotiated rate in the HPT dataset but there are multiple matches and not enough information to distinguish between them. 
### For DRG-872:
* Mount Sinai (not montefiore as indicated in the assignment) lists this drug at 29259.18. We likely do not see this rate in the TIC dataset because it is not fully covered, or is only covered at the generic price. 


## Proposed matching approach
The proposed approach is to group samples by 4 matching keys, and using the fraction of reported payout in the TIC over reported charge in the HPT, plus whatever information we have about the specific plan's coverage, to create a score of confidence for fuzzy matches.

Important keys to match on:
1. Payer (fuzzy match on the name)
2. Hospital ein (there is 1 per hospital, extracted from the filename in 1st column of the hpt dataset)
3. Procedure code (this requires a little clean-up )
4. Procedure code type

Important columns for constructing a match score within each matching subset:
1. Prices: match score should be based on what % of a procedure was covered and what we know about coverage for that procedure (possibly the standard_charge_negotiated_percentage in the hpt dataset)
2. HMO/medicare/other plan types should factor in here: different plans cover different medications at different rates. This can serve as a prior to weight the match score. A reported reimbursement in the TIC of 50% of the procedure cost, when we know that the plan covers 25%, should reduce our confidence in a match.

Important columns for output:
1. Payer
2. Plan type
3. Hospital
4. NPIs
5. Code
6. Code type
7. Negotiated payment rate
8. Actual reimbursement
9. Probably date, setting (inpatient/outpatient).

## Conclusion
My code sketches an outline of an approach to matching rows. Althoguh my confidence score needs work and there may be more specific ways to match the rows, it includes all data from both datasets and attempts to compare the prices between the two datasets. Future work is needed to dig into why the score is greater than 1 in many cases (my assumption was that the rate would be lower than the hospital's negotiated rate) and how better to handle mismatches.
