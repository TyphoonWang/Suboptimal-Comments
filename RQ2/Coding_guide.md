# Tagging Rules

This document describes how we define and tag hunks using our proposed taxonomy. This will include a set of carefully justified rules for resolving ambiguities and conflicts during the tagging process. If you find any part of this document strange/problematic/unconvincing, feel free to discuss with us about how to modify it.

## Taxonomy

This is a three dimensional taxonomy, with **operations** and **content types**. The content types are grouped into three levels. When tagging, we first identify which operation it is, then find out what content type is being changed by the operation.

We can express the formatting and the whole taxonomy in Python like this.

```python
operations = ["adding", "removing", "supplementing", "fixing", "clarifying"]
content_types = {
  "code logic": [
    "function summary", 
    "usage", 
    "context", 
    "rationale", 
    "code file structure"
  ],
  "under development": [
    "TODO",
    "commented code",
    "uninformative"
  ],
  "tool related": [
    "auto-generated",
    "deprecated",
    "directive"
  ],
  "metadata": [
    "link",
    "log"
  ],
}
additional_tags = [
  "translating", "formatting", "adjusting blanklines", 
  "updating tag", "fixing typo", "moving comment", "unknown or error"
]
factors = ["divergence", "tool", "procrastination"]

tags = []
for op in operations:
    for l1_type, l2_types in content_types.items():
        for l2_type in l2_types:
            for reason in factors:
                tags.append("{} {}: {} {}".format(op, l1_type, l2_type, factors))
tags.extend(additional_tags)
```

The `tags` variable describes all the legal tags in our taxonomy, in format `{op} {l1type}: {l2type} {reason}`. Some examples include: `add code logic: function summary divergence`,  `supplement code logic: rationale procrastination`, `fix metadata: link tools`, etc. In the subsequent document, we use `{op}`,  `{l1type}`,  `{l2type}` , `{reason}`as placeholders if they can be multiple values.

## Tagging Rules

Please refer to the paper for general description / definition of the taxonomy. In this section, we will specifically discuss the peculiarities we encountered during tagging,

1. All tagging should be on a **logical element** of comment. Since a hunk might contain multiple logical element, a hunk might have multiple tags. It's up to the tagger to decide what constitutes a logical element, but often it will be a paragraph or a line depending on the context. For example, we can tag the following hunk like this, and then we merge into two tags: `add code logic: function summary` and `add code logic: usage`. In the subsequent section, we use **element** to refer to what we are tagging.

   ```java
   +    /**
   // adding code logic: function summary
   +     * Helper method for creating a folder.<p>  
   +     * 
   // adding code logic: usage
   +     * @param rootPath the root path of the folder 
   +     * @param deep if true, creates all parent folders
   +     * 
   // adding code logic: usage
   +     * @throws CmsException if something goes wrong 
   +     */
   ```
   
2. If an element provide additional information for implementation or development, e.g. “When implementing xxx you should do yyy first,” this should be tagged as `{op} code logic: rationale`.

3. An element should only be tagged as `{op} metadata: link` if there is no other information in this element. For example, these elements should be tagged as `link`,

   ```java
   -     * @see #getCacheSizeBytes()
   -     * @see #getExternalCacheQuotaBytes()
   -     * @see #getExternalCacheSizeBytes()
   ```

   ```java
   - * <a href="RoleSearch.java.html"><b><i>View Source</i></b></a>
   ```

   While this shouldn't. Although it contains a link, it should be classified as `usage` because it is describing return values.

   ```java
   +   * {@link FieldPartitioner}s are returned in the same order they are used
   +   * during partition selection.
   +   * </p>
   ```

4. If an element is only a Javadoc skeleton of `@param`  or `@exception` with only a variable name/type but no description, it should be tagged as `{op} under development: uninformative`, because no usage information is really provided. The peculiarity here is that it's hard to determine whether some skeleton is informative enough, so we take a conservative approach, i.e. every skeleton with no natural language description is uninformative.

5. If a hunk is a commented code block along with comment that describes the commented code or explain why it is commented, we consider it as one element and tag it as commented code.

6. Pay special attention to diff hunks which partially modify a multi-line comment. It could be anything but in many cases it is not obvious from the diff hunk only, and we must analyze the surrounding code.