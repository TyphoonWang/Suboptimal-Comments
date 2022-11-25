# Supplementary materials are divided according to the RQs. for the paper
This repository contains the main data and scripts used in 'Suboptimal Comments in Java Projects: From Independent Comment Changes to Commenting Practices'
The materials are divided according to the RQs.


### RQ1

* Repositories.csv
It contains the matedata of 4,392 GitHub Java open source repositories we used in the study. 

* independent_comment_changes.zip
It contains all independent comment changes we collect from 4,392 Java open source repositories.
** GitHub blocks files larger than 100 MB. You can download the dataset via [Zenodo](https://zenodo.org/record/7360249). 

* javadoc_comment.csv / inline_comment.csv
The number of Javadoc and non-Javadoc changes and ICCs in each repository. 

* comment_parser.py
It used to acquire all changed comment in log files.

* inline_comment.py
It used to retrieve all independent non-Javadoc comment changes, i.e., hunks containing changed non-Javadoc comments but no changed code line.

* javadoc_match.py
It used to match Javadoc changes with code changes within related method/class.

* javadoc_comment.py
It used to retrieve all independent Javadoc comments changes, i.e., changed Javadocs without changed line in correspoding method/class.

* sampled_comments.csv
It contains 400 sampled comments we used to evaluate our heuristics on identifying ICCs.

### RQ2

* Thematic_analysis_results.csv
It shows the thematic analysis results for RQ2. It contains all sampled comment changes for our thematic analysis and their initial codes and final codes.

* Code_book.md
It shows the code book for thematic analysis results for RQ1.2.

* Coding_guide.md
It shows more details about how we conduct the coding. 



### RQ3

* Guidelines_thematic_analysis_results.csv
It contains commenting related guidelines we collect from 600 sampled repositories and results we labelled.

* Commenting_Guidelines_Codebook.docx
It is the code book for the analysis on commenting guidelines.

* guideline_pages.zip
It contains all pages with commenting guidelines in 600 sampled repositories.

* check_violation.py
It is the script we used to check violations.

* Issues.csv
It contains the 24 issues we opened and responses from developers.


### RQ4

* get_javadoc_adoption.py / get_checkstyle_adoption.py
The scripts we used to investigate the use of Javadoc and Checkstyle.

* javadoc_adoption.csv / checkstyle_adoption.csv
It contains our investigation on if repositories incorporate Javadoc/Checkstyle into pom.xml/build.gradle, and if they provide Checkstyle configuration file. It also contains when related code is introduced.

* survey-results.docx
It contains our design of the survey and results from respondents.