# CHANGELOG

## 2025-08-27

### New Filters

- Amazon
  - (Mobile) Item listing - Similar products (Sponsored)
  - (Mobile) Injected pagination ads
- Bing - ad next to image result
- Google
  - Discussion and Forums list items for Facebook groups
  - Right sidebar Feedback link
  - Search bar - Search suggestions dropdown menu disclaimer about reporting inappropriate predictions
  - Search toolbar - tabs - Short videos
  - (Mobile) Images section in standard search results
  - Alternate version of AI summary filter
- Imgur
  - Navbar game icon
  - Suggested content below posts
- IPTorrents - Began filtering parent class of all top banner ads as the individual filters all descended from the same parent class
- Next.Invitation.Codes - various filters to simplify cluttered interface and remove nags
- Reddit - User drawer - Earn cash on Reddit
- Twitter/X
  - (Mobile) Floating action button
  - (Mobile) Bottom navbar - Grok button
  - Main feed - inline Grok buttons

### General cleanup & optimization

- Completely re-organized all Google, LinkedIn, and Reddit filters among many others
  - Grouped filters to better reflect page structure and purpose
  - Removed redundant descriptors such as "hide," "remove," etc.
  - Removed unnecessary punctuation and formatting, e.g. quotation marks
  - Flattened tree structure to reduce unnecessary empty lines or new lines when sections only contained a single filter
- Replaced previous Google filter for Short Videos as it was causing all search results to be hidden when not on mobile devices.
- Re-wrote two ChatGPT filters to be consistent with recent site updates
- Removed duplicate filters for VinstarTheme.com.
- Removed deprecated filter for ChatGPT disclaimer text.
- Removed filters for Twitter/X that no longer work or were problematic.

## 2025-07-27

FIX: Rollback Google filter in previous update to correct regression causing all Google search results to be hidden.

## 2025-07-26

### New filters

- Google
  - Updated AI Mode tab filter, new version credit to [u/RraaLL](https://www.reddit.com/r/uBlockOrigin/comments/1l4vpmj/comment/mwcvxlt) on [r/uBlockOrigin](https://www.reddit.com/r/uBlockOrigin)
  - Short Videos section (two versions - require further optimization but functional for now)
  - Videos section
- Reddit - Added filters for Advertise on Reddit and Reddit Pro link in user drawer
- Additional filters added for: Dispatch, Dribbble, Ebay, IPT, Winmoes, xahlee.info Unicode search

### General cleanup & optimization

- Alphabetized the less organized section
- Google
  - Youtube videos section - Temporarily disabled as it was causing unintended issues when using reverse image search.
  - Grouped mobile-specific filters together
- Reddit - Optimized and organized filters for user drawer
- Promoted Lenovo and TechRadar to Cosmetic Filters section

## 2025-06-20

### New filters

- Amazon
  - Amazon Pharmacy promotion above item images
- Google
  - "Google Sponsored" promotional ad for Developers Console which appeared when I searched using 'site:'
  - "Save your favorite brands to get more relevant results"
  - "Popular products" section
  - AI Mode toolbar tab
  - AI Mode popup nag/ad
- Mozilla
  - Firefox News ad
- The Noun Project
  - In-line ad
- News.com.au
  - Sticky PIP video player
- Reddit
  - Top toolbar - 'Advertise on Reddit' button
  - Mobile - "Related Answers" section after comments
- Vecteezy
  - Sponsored search results

### GENERAL CLEANUP & OPTIMIZATION

- Temporarily disabled Google Chrome search filter
- Removed 'www' subdomain from This Week News filters
- Amazon
  - Reformatted Amazon navigation menu filters to improve readability
  - Removed disabled poorly optimized filter for "Buy it again" on the 'Your Orders' page
  - Reformatted note regarding "Customers also bought" widget for clarity. Enabled hiding items within the widget, disabled hiding the entire widget.
- Moved Vecteezy to the organized Cosmetic Filters section

> [!NOTE]
> Changes prior to June 2025 were not tracked in detail. See git log for changes.
