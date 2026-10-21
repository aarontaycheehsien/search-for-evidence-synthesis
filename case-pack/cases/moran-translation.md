# Translation case: one search, two databases (Moran et al., 2021)

For Chapters 2, 7 and 11. Built on 2026-10-21.

## Source

The strings below are quoted, for teaching and with attribution, from the authors' search script (`01_conditiontreatments_search.R` in `NPMoran/metah06_condition-dependence-of-boldness_OSF`, commit `b25a3c2`). The review is Moran et al. (2021). Claims about database behaviour cite the dated entries in [`claims/register.csv`](../../claims/register.csv); re-check them before teaching, because vendors change their documentation.

**Web of Science Core Collection, update search of 4 February 2019, as echoed by the database ("You searched for:"):**

```
TS=("*nutrition*" OR "*nourish*" OR "calori*" OR "hunger" OR "starv*" OR (("diet*" OR "food") NEAR/10
("quality" OR "restrict*" OR "depriv*" OR "enrich*" OR "availab*" OR "manipul*" OR "limit*")) OR "bod* state*"
OR "bod* condition*" OR "condition depend*" OR "state depend*" OR "asset protection" OR "residual reproductive value")
AND TS=("bold*" OR "explorat*" OR "risk*" OR "novel*" OR "predat*" OR "refuge" OR "neophobi*" OR "neophil*")
AND TS=("personalit*" OR "temperament*" OR "coping style*" OR "behavio* type*" OR "behavio* strateg*"
OR "behavio* syndrome*" OR "risk-taking behavio*" OR "developmental plasticity" OR "phenotypic plasticity"
OR ("behavio*" NEAR/5 ("animal*" OR "plasticity" OR "flexibil*" OR "trait*" OR "phenotyp*" OR "response*" OR "decision*")))
```

**Scopus, update search of 4 February 2019, as recorded in the script:**

```
TITLE-ABS-KEY ( "*nutrition*" OR "*nourish*" OR "calori*" OR "hunger" OR "starv*" OR ( ( "diet*" OR "food" ) W/10
( "quality" OR "restrict*" OR "depriv*" OR "enrich*" OR "availab*" OR "manipul*" OR "limit*" ) ) OR "bod* state*"
OR "bod* condition*" OR "condition depend*" OR "state depend*" OR "asset protection" OR "residual reproductive value" )
AND TITLE-ABS-KEY ( "bold*" OR "explorat*" OR "risk*" OR "novel*" OR "predat*" OR "refuge" OR "neophobi*" OR "neophil*" )
AND TITLE-ABS-KEY ( "personalit*" OR "temperament*" OR "coping style*" OR "behavio* type*" OR "behavio* strateg*"
OR "behavio* syndrome*" OR "risk taking behavio*" OR "developmental plasticity" OR "phenotypic plasticity"
OR ( "behavio*" W/5 ( "animal*" OR "plasticity" OR "flexibil*" OR "trait*" OR "phenotyp*" OR "response*" OR "decision*" ) ) )
AND ORIG-LOAD-DATE > 20181110
```

Line breaks are added for reading.

## What looks the same and is not

| Feature | Web of Science | Scopus | What to check |
|---|---|---|---|
| Fields searched | `TS=` covers title, abstract, author keywords and Keywords Plus (`wos-ts-fields`). Keywords Plus are words harvested from the titles of the articles a record cites (`wos-keywords-plus`) | `TITLE-ABS-KEY` covers title, abstract and keywords, where keywords include author keywords and index terms (`scopus-title-abs-key`) | A Web of Science record can match on words that appear only in the titles of works it cites; a Scopus record can match on assigned index terms. Neither is in the record's own title or abstract |
| Quotation marks | Exact phrase (`wos-phrase`) | Loose phrase: punctuation ignored, plurals and spelling variants included, wildcards allowed (`scopus-loose-phrase`) | Whether Web of Science applies wildcards inside quoted phrases such as `"bod* condition*"` is not stated on the pages checked |
| Leading truncation, `"*nutrition*"` | Allowed in Topic searches with at least three characters after the wildcard (`wos-left-truncation`) | Allowed anywhere in a word (`scopus-wildcard-position`) | Both accept it; the minimum-length rule matters for shorter stems |
| Proximity | `NEAR/10`: within 10 words (`wos-near`) | `W/10`: within 10 words, any order (`scopus-proximity`) | Close equivalents. Web of Science does not allow `AND` inside a `NEAR` group |
| Hyphens | `"risk-taking behavio*"` in the update string | `"risk taking behavio*"`; in a loose phrase, a hyphenated form is treated as the loose phrase (`scopus-loose-phrase`) | How Web of Science treats the hyphen was not confirmed from its documentation |
| Plurals | Wildcards used throughout | Lemmatisation applies anyway unless an exact phrase is used (`scopus-lemmatisation`) | Some Scopus wildcards are redundant for plurals but still widen matching |
| Operator order | Parentheses used throughout | Processed as OR, then W/n and PRE/n, then AND, then AND NOT (`scopus-proximity`) | The full parenthesisation protects the string; removing it would change the Scopus result |
| Updating method | Whole search re-run, then compared with the first results by exact title: 92 new | `ORIG-LOAD-DATE > 20181110`: 42 new | See exercise 4 |

## Exercises

**1. Fields.** Describe a record that Web of Science would retrieve and Scopus would not, for the same terms, using only the field differences above. *Worked answer:* a paper whose title, abstract and author keywords never say "boldness", but which cites papers with "boldness" in their titles; Keywords Plus may then contain the term, so `TS=` matches it. The reverse case is a record whose Scopus index terms contain a term absent from its title, abstract and author keywords.

**2. Which string was run?** The script's comment for the first Web of Science search (10 November 2018) reads `"asset protection" residual reproductive value")`. *Worked answer:* the comment was typed, not copied; the quotation marks do not balance, and the string the database echoed in the update search is correct. Treat the comment as a documentation slip, and record executed strings by copying them from the database's search history. Appendix S2 of the article's supporting information is where the published strings should be checked.

**3. Initial and update strings differ.** The first Web of Science search used `"risk taking behavio*"`; the update used `"risk-taking behavio*"`. *Worked answer:* an update is only comparable with the first search if the strategy is identical or the change is reported and its effect checked. Here the effect depends on Web of Science's hyphen handling, which the documentation checked does not settle; test both forms and report the difference.

**4. Two update methods.** *Worked answer:*
- The Web of Science comparison by exact title counts as new any earlier record whose title has since changed by one character, and treats as old any new record whose title exactly repeats an earlier one.
- The Scopus limit `ORIG-LOAD-DATE > 20181110` takes records loaded after 10 November 2018 regardless of publication date, so it includes older papers loaded late. A record loaded later on 10 November itself, after the first search ran, would satisfy neither search, because `>` excludes that day.
- Neither method is wrong, but they answer different questions ("what is new to our results?" against "what is new to the database?"), and the report should say which was used.

**5. Deduplication.** See [`case-pack/data/moran-2021/README.md`](../data/moran-2021/README.md): the 7,208 initial records leave between 5,390 and 5,552 after deduplication, depending on the rule. Ask readers which number they would put in a PRISMA flow diagram and how they would describe the rule.

## Reference

Moran, N. P., Sánchez-Tójar, A., Schielzeth, H., & Reinhold, K. (2021). Poor nutritional condition promotes high-risk behaviours: A systematic review and meta-analysis. *Biological Reviews, 96*(1), 269–288. https://doi.org/10.1111/brv.12655
