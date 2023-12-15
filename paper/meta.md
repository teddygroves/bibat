This page has instructions from the Journal of Machine Learning Research

# Machine Learning Open Source Software

Open source tools have recently reached a level of maturity which makes them
suitable for building large-scale real-world systems. At the same time, the
field of machine learning has developed a large body of powerful learning
algorithms for a wide range of applications.

JMLR is proud to support the open source movement by having a track on open
source software in machine learning. The aim of this special section is to
provide, in parallel to theoretical advances in machine learning, a venue for
collection and dissemination of open source software. Having a resource of
peer reviewed software accompanied by short articles allows to build a common
repository of high quality machine learning software that are endorsed by the ML
research community.

We encourage submissions which are contributions related to implementations
of non-trivial machine learning algorithms, toolboxes or even languages for
scientific computing. The software must adhere to a recognised open source
license (http://www.opensource.org/licenses/). Evidence of an active user
community should be demonstrated in the cover letter by, for example, number
of active developers, number of stars on github or similar metrics. As with the
main JMLR papers, all published papers are freely available online. Submissions
should clearly indicate that they are intended for this special track in the
cover letter of the submission.

Since we specifically want to honor the effort of turning a method into a highly
usable piece of software, prior publication of the method is admissible, as
long as the software has not been published elsewhere. If the software has been
the main content of a paper appearing in a peer reviewed conference or journal,
then there should be a document in the code repository (referred to in the
cover letter of the submission), listing the software package's improvements
and extensions. It is hoped that the open source track will motivate the machine
learning community towards open science, where open access publishing, open data
standards and open source software foster research progress.

## Format

We invite submissions of descriptions of high quality machine learning open
source software implementations. Submissions should at least include:

1. A cover letter stating that the submission is intended for the machine
learning open source software section, the open source license the software
is released under, the web address of the project, the software version to
be reviewed, and evidence of an active user community. It is particularly
appreciated if it includes suggestions of possible reviewers, explaining briefly
why they are relevant to your work.

2. An up to four page description based on the JMLR format, with additional
pages for references.

3. A zip or compressed tar-archive file containing the source code and
documentation in addition to an optional link to a code repository.

## Submission checklist

- [] Ensure the submitted code compiles and runs on all your supported
platforms.

- [] Ensure the licensing terms of all included components comply with the open
source definition and are clearly stated in the source package and mentioned in
each source file.

- [] Ensure the source package contains no extra files, such as version control
system files or '._' property files. (Remember that some of these may not be
visible on your own platform.)

## Review Criteria

The following guidelines would be used to review submissions. While ideally
submissions should satisfy all the criteria below, they are not necessary
requirements.

### The four page summary

1. The quality of the four page description.

### The impact on the machine learning community

1. The novelty, breadth, and significance of the contribution.

2. Evidence of an active user community (documented in the cover letter, not
the paper).

3. The openness of the project, such as a public source code repository, bug
tracker, mailing list/forum, that allows new developers to participate and
contribute.

4. The quality of comparison to previous (if any) related implementations,
w.r.t. run-time, memory requirements, features, to explain that significant
progress has been made.

### User documentation

In assessing the documentation, reviewers should consider presence and quality
of:

1. Installation instructions

2. Tutorials to show simple use-cases and on-board new users.

3. Non-trival examples of typical use-cases of the software.

4. Full documentation of the API. Reviewers should also consider how easy it is
to view the documentation, for example whether it is available as a website, or
requires building documentation locally to view it.

### Openness to new developers / Ease of contribution / Sustainability

1. How easy is it for new contributors to participate / contribute.

2. The clarity of software design.

3. The quality of the developer documentation (should enable easy modification
and extension of the software, provide an API reference)

### Implementation and adoption of software development best practices

1. Extensive unit and integration testing, and report of code coverage of tests.
It is expected that test coverage is close to 100%.

2. Continuous integration, ideally on all supported platforms and with multiple
versions of potential dependencies.

1. The breadth of platforms it can be used on (should include an open-source
operating system).

1. The freedom of the code (lack of dependence on proprietary software).

## Accepted Papers

After acceptance, the abstract including the link to the software project
website, the four page description and the reviewed version of the software will
be published on the JMLR-MLOSS website http://www.jmlr.org/mloss. The authors
can then make sure that the software is appropriately maintained and that the
link to the project website is kept up-to-date. When preparing this information,
follow the JMLR instructions for formatting final sumbmissions. In addition
to the LaTeX source, MLOSS authors must submit an single file containing an
archive of the source code that will be published on the JMLR website. This
file should be named according to the JMLR author conventions, for example
jones03a-code.tar.gz.
