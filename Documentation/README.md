# This program will generate the mock data to meet the requirements stated in our "Data Analysis Objectives.md" file.

---

## Applicant information
1. Application submission date (prevYear: LateAug,Oct,Nov,Dec || thisYear:Jan-MidMar)
2. --> 20% of applications: Aug–Oct 2022
       60% of applications: Nov 2022–Jan 2023
       20% of applications: Feb–Mar 2023
3. --> Days opened (how long it took to submit application)
4. Application id
5. Name
6. Program (Associates, Bachelor, Master, MBA, PhD, Undecided)
7. Application status (admitted, applied, enrolled, lost, rejected, under review, withdrawn)
8. --> Applied (total) — 100% (base)
       Admitted (offer made, undecided): 70%
       Rejected: 30%
       Enrolled (matriculated): 50%
       Under review: 3%
       Lost (admitted but declined / accepted elsewhere): 26%
9. Age (May include age ranges: <18, 18-21, 22-25, 26-30, 30+)
10. Gender (M, F, Other)
11. Ethnicity
12. Nationality (Brazil, China, France, Germany, India, Nigeria, UK, USA, Other)
13. --> IF US, State?
14. Scholarship (Yes, No)
15. First Generation (Yes, No)

```
                    APPLIED
                     100%
                /            \
           ADMITTED         REJECTED
             64%               36%
      /       |        \
ENROLLED  UNDER-REVIEW  LOST
  65%          5%        30%
                          |
                      WITHDRAWN
                         14%

```

| Admission Cycle               | Approx. Months            | Description                              |
|-------------------------------|---------------------------|------------------------------------------|
| **Application Opening**       | **August–October 2022**   | Applications for Fall 2023 open.         |
| **Peak Submissions**          | **November–January 2023** | Most students submit around deadlines.   |
| **Late/Extended Submissions** | **February–March 2023**   | Late or rolling admissions still active. |
| **Decisions Sent**            | **March–April 2023**      | Offers go out.                           |
| **Enrollment Confirmation**   | **May–June 2023**         | Students commit for Fall 2023 start.     |

