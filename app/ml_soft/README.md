# MML Syntax Checker

### Problem Statement

This problem requires you to write a program to syntactically validate some simple documents written using _M Markup Language_ (MML). 
MML is a subset of HTML that introduces some structural simplifications: 
- Attributes are not allowed.
- Escape characters are not allowed.

In these documents you'll find ordinary text, with arbitrary line lengths, interspersed with markup tags. The markup tags we consider will generally occur in pairs, or be self-closing (eg `<TAG />`). 

Example:
```
This is some ordinary text. <IAMATAG> text <BOLD>
other text </BOLD>
more text </IAMATAG> 
```
There are two pairs of markup tags in the example: IAMATAG and BOLD. A markup tag may contain text content and other tags.

The end of the document region affected by the tag is indicated by a tag with the same name which begins with a slash (for example `</IAMATAG>`). Tagged regions may encompass more than one line of text. 

## Your Mission, Should You Choose To Accept It
- Create an syntax validator in 3 test-driven phases.
- Each phase will tackle a particular set of validations.
- The main objective is to end up with clean, simple code that correctly validates the given inputs.
- Each phase should be the minimal amount of code to satisfy the test cases.
- A colleague has already created a set of tests that check your validator. 


### Phase 1 - detect invalid tags
- A tag must be opened by `<` or `</` and must be then closed by a `>` character (`<HELLO`, `</HI` are invalid)
- A tag name must have at least one, and no more than 10 characters (`<HELLOOOOOOOOOO>` is invalid)
- A tag name must be upper-case and alphabetic. (`<HELLO-1.0>`, `<hellow>` are invalid)
- Content must not include dangling `>` characters. (`this is some content>` is invalid)

### Phase 2 - detect incorrectly balanced tags
- Tags must exist in correctly balanced and nested pairs.
- Valid example: `<A><B></B></A>`
- Invalid example: `<A><B></A></B>`

### Phase 3
- The special `CDATA` tag must be supported. This tag contains text content which must not be validated. 
- CDATA tags must open with `<![CDATA[` and must be closed with `]]>`

Example:
```
<![CDATA[Within this block we can use any tags like <foo> and <bar> and they will not be validated.]]>
```

