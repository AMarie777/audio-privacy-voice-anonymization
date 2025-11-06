[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Try5IhwB)
# CS 1657: Privacy in the Electronic Society

## Project 2

Released: Tue, Nov 04

Proposal discussion: Thu, Nov 06, start of class

Proposal due: Tue, Nov 11, 11:59 PM

Final report due: Tue, Dec 02, 11:59 PM

### Motivation

In this course, we've discussed many aspects of digital privacy. We’ve discussed
*authorization* at length, including multiple factors that can be used for
authentication, several approaches to representing and enforcing access control
policies, and the use of disk encryption and/or secure boot to prevent specific
subversions of authorization systems. We’ve also discussed differential privacy
and other techniques for obfuscating/anonymizing data releases. In this project,
you will explore an issue related to digital privacy in a hands-on way.

For instance, you may consider:

- implementing and testing a prototype enforcement engine for an access control
  policy language of your choice, studying the benefits and drawbacks to
  including advanced features
- comparing the psychological acceptability of various biometric authentication
  factors
- developing and analyzing a sophisticated brute-force approach to breaking a
  disk encryption scheme
- comparing secure boot strategies used in video game consoles vs. smartphones
- comparing the application of k-anonymity vs. differential privacy when
  studying one or more specific data sets
- comparing original differential privacy with proposed relaxations and/or other
  quantitative measures of privacy

Your final submission should consist of the following components.

- Any code that you wrote for the project, satisfying the C tasks in your
  proposed outline. Code can be written in the language of your choice (check
  with your instructor if you’re not sure it will work for them).
- A writeup that explains the motivation behind the project, the experiment(s)
  carried out, the results, and an interpretation of the results. The writeup
  should satisfy the W tasks in your proposed outline **and** discuss your
  approach to the C tasks, mentioning specific lines, function names, etc. to
  help us understand your code. Each task should be discussed in your writeup.

All features, bugs, and other details regarding your code should be made clear
in your writeup (i.e., do not include such details in a separate README or
expect us to read every comment in your code). Each writing task should be
clearly titled, and each code task should be clearly discussed in the writeup.
In short, do not make us search for the components of your submission. Show off
the hard work you did!

You may work individually or in a group of 2 or 3. If you work in a group, make
sure all members use the GitHub Classroom link to join the repository. (One
member should create the team, then the other(s) should join the existing team.)
You do *not* need to work in the same group for all projects throughout the
semester.

### Proposal

Before the proposal deadline above, submit a proposal in PDF format that
explains the goals of your project and any preliminary results you have to
demonstrate that the project is worth pursuing. Your goal during the proposal
period is to start working on your project seriously, while also documenting
your work so that you can receive feedback on what you're planning for the
remaining time. This means that **the proposal write-up should not be the only
thing you work on** during this time; get started on the actual project!

First, consider the overarching theme of your project. **What questions do you
want to answer?** Think about our high-level course goals as well as your
individual goals, and how answering these questions will support those goals.

As you develop your proposal and describe your plan, consider how you will
satisfy three high-level criteria:

1. Technical depth: What is the intellectual merit of this project? How do you
know that it will be sufficiently challenging, based on what you've done so far?
If some steps are easier than expected, what will you add to compensate? If some
steps are more challenging and you cannot complete everything, what will you
prioritize?

2. Topic relevance: What are the privacy impacts of this project? What will you
hope to learn about privacy by completing it, and what evidence do you have that
it will be successful? What alternative options will you explore if your plan
does not work, or you otherwise need to pivot?

3. Support of goals: Think about your individual course goals that you laid out
in the Preliminary Reflection. How does this project contribute to you achieving
your goals? What challenges do you foresee, and what adjustments will you make
to ensure progress toward your goals if things go wrong?

In addition to answering the above, your proposal should include an outline of
the writeup that you will submit at the end of the project. Lay out each code
and writing task that you will complete. For each one, specify what steps you
will complete and what you hope to learn (and explain to us!) by doing so. Show
any results that you have collected so far that demonstrate the feasibility and
impact of each task.

An example outline is available below with suggested things to include, but **we
encourage you to think beyond these guidelines** if you have ideas that don’t
fit into what we suggest.

As explained above, during the proposal period, you should be actively working
on the project, not just brainstorming ideas for the proposal. You should
explore the topic in a hands-on manner, especially if you have multiple ideas
and/or are unsure if your ideas will work. During this period, **it is your
responsibility to experiment** and determine what you will be able to complete
by the deadline. Plans can always change for a variety of reasons, but your
proposal should be well-thought-out and based on having made a reasonable amount
of progress toward the project you intend to complete.

To support you in developing your proposal, we will reserve time in lecture (as
scheduled above) to discuss everyone's (early) project ideas. To get the benefit
of this session, you are responsible for attending this session and being
prepared to discuss your project idea.

Submit your proposal as the only PDF file contained directly within the
`proposal` subdirectory. Your submission must be committed and pushed before the
proposal deadline above.

Within a few days after the proposal deadline, you will receive written feedback
on your proposal, formalizing the standard by which your final submission will
be evaluated. You should keep working on your project in between! Our goal is to
give suggestions to ensure your project is strong, not force a change in your
idea.

In our feedback, we may include questions that come to our minds as we read your
proposal. We are not suggesting that you should already know the answers, or
that these are things we think you should have included. Rather, we are sharing
questions we recommend exploring as you continue work on your project. We are
trying to help you brainstorm things to consider as you develop your own ideas
and respond to what you find interesting about the results.

### Example Outline 1

This section contains an example outline of tasks geared toward exploring the
advantages and disadvantages of certain types of expressiveness of access
control systems. Task W0 introduces an access control language, and Task W1
fully specifies the syntax you will use to represent it. Task C2 demonstrates
how the language can be interpreted and enforced. Tasks W3, W4, and W5 give
specific examples and use cases for the main features of the language. Tasks C6
and W7 study how policies with differing levels of complexity effect the
efficiency of enforcement.

**Task W0:** Choose an access control language, perhaps one based on ABAC,
ReBAC, SD3, or RT. Describe the features that your implementation will support,
which make it relevant to a scenario that you are investigating, such as:

- *Indirection*: The ability to assign a large set of permissions at once.
  Consider roles, attributes, groups, etc.
- *Administrative Delegation*: The ability to set additional entities that have
  the ability to affect a resource’s access policy. For example, consider RT’s
  delegation of attribute authority, or the $ notation in SD3. You might
  represent different administrative entities as different text files, each
  representing the relations published by one particular entity.
- *At least one other*: At least one other feature that allow administrators to
  write expressive policies. Consider role inheritance (role hierarchy),
  attribute intersection, parameterized attributes, etc.

To start your writeup, overview the access control system that you chose, the
features it supports, and any extra tools you developed.

**Task W1:** Fully describe the syntax used to write a policy file for your
access control language. This file should be plaintext and simple for an
administrator to write. This means that your policy should *not* be hardcoded in
the program. One should be able to adjust the policy without changing or
recompiling the code.

Explain how each supported feature is represented in plaintext. If your file
needs to include a list of all existing users/subjects or
files/resources/objects, explain the format for this information as well. Your
format is allowed to consist of multiple files (e.g., delegated attributes may
be declared in separate files).

If your access control system is inspired by an existing language, note that the
syntax used in your policy file may differ from how we viewed example policies
in class. For instance, you may use `<-` or `:-` to represent RT’s `←` symbol.
Alternatively, you may consider standard formats for structured input, which
would enable you to utilize existing parsing libraries. Consider JSON, XML,
Datalog, etc. Again, you **do not** need to type your policies in the exact
format that existing languages use.

To give one simple example using XML, you might represent `Pitt.student ←
Juliana` as follows:

    <attribute name="student" domain="Pitt" constant="Juliana">

**Task C2:** Implement a program to interpret your access control language. It
should be able to do the following steps:

1. Read, parse, and preprocess (if necessary) a specified policy file(s) in the
   format you describe in Task W1.
2. Prompt the user for an access query (that is, a query of the form, “Can user
   *u* access file *f* with *read* privilege?” or similar). Clearly state the
   format in which the user must type their query.
3. Using the policy that was parsed from the input file, determine whether the
   access should be permitted, and output the response (*allow* or *deny*).
4. Repeat from Step 2.

Note that you are only required to support access queries, but you can implement
additional queries for extra credit (e.g., “Is user *u* a member of role *r*?”).

**Task W3:** Explain, with examples, how *indirection* is represented, and how
it should be used, in your language. You should give at least 2 examples to make
it clear how this feature works and how it can be used.

Discuss the benefits to having this feature, from the perspective of privacy,
expressiveness, efficiency, administrative overhead, usability, or some other
metric. Does it allow for easier assignment of certain types of permissions?
Will it prevent errors in the policy? Does it allow users to set policies that
more closely match their preferences? Does it allow resource owners to set
policies they could not without the feature, and therefore support more diverse
types of privacy requirements?

Next, discuss the potential drawbacks of having this feature, again considering
privacy, administrative overhead, usability, and/or other metrics. Could it make
it slower to render access decisions? Could it give the user too many options
and potentially overwhelm them? Could it be misunderstood and lead users into
granting accesses they did not intend to? Could it prevent, or make more
complex, an automated analysis to detect insecure policies? Consider specific
scenarios wherever possible.

**Task W4:** Explain, with examples, how *administrative delegation* is
represented and used in your language. Again, you should give at least 2
examples.

Discuss the benefits and potential drawbacks of having this feature, similar to
how you did in Task W3.

**Task W5:** Name any other access control features that you implemented in your
program (at least one is required). Explain, with examples, how they are
represented and used in your language. As before, give at least 2 examples of
each feature.

Discuss the benefits and potential drawbacks of having each additional feature,
similar to how you did in Task W3.

**Task C6:** Construct at least 5 *experimental policies* (manually written or
randomly generated) of varying size/complexity. Your goal is to study the
efficiency of enforcing policies of various complexities to investigate how your
enforcement program scales to large, complicated policies. Consider, for
instance, long chains of trust.

Write a program to time (benchmark) your processing of a policy and query. This
program should not be interactive and should run hardcoded (or randomly
generated) queries on the policies you constructed, then report the results.

You might consider measuring separately the time for two distinct tasks for each
policy, if it makes sense for the implementation you wrote:

1. The time it takes your program to read and preprocess the policy, without
   considering queries.
2. The time it takes your program to respond to a query *after* the policy has
   been read and processed.

You are welcome to adjust this according to your particular implementation
strategy; what makes the most sense to get a detailed picture of your
implementation’s efficiency as policies scale?

Use the average of multiple trials if your timing is not consistent.

**Task W7:** Interpret the results of Task C6. Show a chart, table, or graph of
your data. Explain what this tells you about how your enforcement engine scales.
If the runtime scales poorly, is this a problem with the language you chose, or
with your specific enforcement engine? Is this language reasonable to use for
personal computers? What about enterprise scenarios? Can it scale to a large
cloud storage service? Show off as much as you can regarding what this
experiment taught you about access control enforcement.

### Example Outline 2

This section contains an example outline of tasks geared toward comparing the
group-based anonymization approaches (like $k$-anonymity) with the statistical
approach (differential privacy) using a single dataset. Task W0 introduces a
dataset, and Task W1 describes possible privacy issues with sharing it
unmodified. Task C2 uses $k$-anonymity or another group-based approach to
anonymize the dataset, and Task W3 explains and interprets the results. Task C4
extracts a specific insight from the dataset, and W5 describes possible privacy
issues with sharing even just this insight. Task C6 modifies the algorithm from
Task C4 to satisfy differential privacy, and Task W7 explains and interprets the
results.

**Task W0:** Identify a publicly-available dataset containing both
quasi-identifiers (e.g., location, age, gender) and potentially sensitive fields
(e.g., preferences, medical conditions, interests). You may consider, for
instance, datasets available at [Academic Torrents](http://academictorrents.com)
or [Kaggle](https://www.kaggle.com).

To start your writeup, describe the source of your dataset and the content
contained therein. You should also provide a link from which the dataset can be
downloaded. **Please do not upload large datasets to GitHub** that can be
accessed elsewhere.

**Task W1:** Describe how the release of this dataset in its current form
reveals potentially sensitive information, and how this information could be
linked back to the users involved through quasi-identifiers and an adversary’s
side knowledge.

**Task C2:** Transform the dataset so that it satisfies $k$-anonymity (or, at
your discretion, another group-based approach, such as $l$-diversity or
$t$-closeness), for some value of $k$. As we discussed in lecture, this should
involve clustering based on quasi-identifiers and generalizing those attributes
to provide the desired privacy metric. Explain in full how you accomplished the
desired property.

**Task W3:** Compare the original dataset to the output from Task C2. In what
ways is less information revealed through this transformation? What information
may still be revealed? Is the utility of this transformed dataset decreased
relative to the original? Are there fields that certain attackers may know that
you did not consider QIs? What would be the impact of this? Give examples as
needed to clarify.

**Task C4:** Implement an algorithm to extract a particular insight from the
data.

**Task W5:** Describe the algorithm implemented in Task C4 and explain why it
does not satisfy differential privacy. In what way might the adversary
differentiate between two neighboring datasets $D$ and $D^\prime$ with high
confidence, given an output from this algorithm?

**Task C6:** Implement a variant of your algorithm from Task C4 that yields the
same insight in a way that satisfies $\varepsilon$-differential privacy, for
some value of $\varepsilon$. As we discussed in lecture, one way to accomplish
this is to add Laplacian noise to the value.

Keep in mind that this requires you to reason about the maximum impact a single
user can have on the output! If a single user can change the output by up to
$A$, you need to sample from a Laplacian distribution with a scale parameter of
$A \cdot b$ to achieve $\frac{1}{b}$-differential privacy.

**Task W7:** Interpret the result and outputs of Task C6. In what way does this
algorithm respect the privacy of the users represented in the dataset more than
the algorithm used in Task C4? Has the utility been impacted, or is the insight
equally valuable? You may wish to run the algorithm multiple times, to
understand the distribution of values that it is likely to output (rather than
analyzing just a single sample, which may be atypical).

### Project Choice

We believe that more interesting results, and more genuine learning, will occur
if you explore the goals of this project in a unique way that is compelling to
you in particular. Give yourself the space and time to consider ideas that are
creative and interesting to you, and that help the reader (us!) learn something
new about privacy.  Whatever you choose to experiment with, you should have
concrete questions you wish to answer, and you must be able to observe, reflect
on, and interpret the results.

### A Final Reminder

As this course is an upper-level elective, you are being given a lot of freedom
in terms of how you tackle this project. In exchange, you also have a lot of
responsibility to demonstrate your hard work adequately to your instructor. As
such, you should include tasks in your outline in which you discuss the most
interesting and relevant portions of your code in detail. Your discussion should
closely align to, and refer to, your specific implementation. (Do not claim that
your code does something that you know it does not — see the Academic Integrity
Policy.)

Your submission should demonstrate three main criteria:

1. Technical depth: What is the intellectual merit of this project? Demonstrate
that you achieved something sufficiently challenging.

2. Topic relevance: What are the privacy impacts of this project? Demonstrate
what you learned about privacy by completing it and why it is meaningful.

3. Support of goals: How does this project contribute to you achieving your
individual goals in the course? Demonstrate the ways in which this project
helped you grow, and in what ways this aligns with the goals you set.

Show us that you’ve thought hard about privacy topics we've discussed in this
course, and that you've taught yourself something valuable about them in the
process.

### Submission

Submit your writeup as the only PDF file directly contained within the `report`
subdirectory. Your submission must be committed and pushed before the deadline
above. Any relevant code that is discussed should also be included in your
commit.

