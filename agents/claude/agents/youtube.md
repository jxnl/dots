# YouTube Processing Agent

## Purpose
Automate YouTube video processing workflow: extract transcripts, download videos, extract frames, and organize files for study note creation.

## Usage

### Full Processing Pipeline
```bash
# Process complete video with auto-detected frames
uv run python yt_processor.py "https://www.youtube.com/watch?v=VIDEO_ID" --auto-frames

# Process with specific timestamps  
uv run python yt_processor.py "https://www.youtube.com/watch?v=VIDEO_ID" --frames "90,400,560,780"

# Transcript only (no video download)
uv run python yt_processor.py "VIDEO_ID" --skip-video --auto-frames
```

### Quick Commands
```bash
# Get video info first
uv run python yt_processor.py info "VIDEO_ID"

# Just transcript + video (no frames)
uv run python yt_processor.py "VIDEO_ID" --skip-frames

# Custom output directory
uv run python yt_processor.py "VIDEO_ID" --output-dir "custom-videos" --auto-frames
```

## What the Script Does

1. **Extracts video ID** from any YouTube URL format
2. **Gets video metadata** (title, duration) for proper naming
3. **Extracts transcript** using `youtube-transcript-api`
4. **Cleans transcript** (saves ~65% tokens) using `clean_transcript.py`  
5. **Downloads video** in 720p using `yt-dlp`
6. **Auto-detects frame timestamps** from transcript (looks for "slide shows", "you can see", etc.)
7. **Extracts frames** using `extract_frame.py` batch mode
8. **Organizes files** into proper directory structure

## Output Structure
```
videos/
└── video-title-sanitized/
    ├── Video Title.mp4
    ├── raw_transcript.txt          # Original JSON format
    ├── raw_transcript_clean.txt    # Token-efficient format
    └── images/
        ├── slide_90s.jpg
        ├── slide_400s.jpg
        └── ...
```

## Key Features

- **Auto-detection of slide timestamps** from transcript content
- **Proper file naming** (converts to lowercase-with-hyphens)
- **Progress tracking** with rich terminal output
- **Error handling** for each step
- **Token optimization** (65% size reduction on transcripts)
- **Flexible frame extraction** (manual timestamps or auto-detect)

## Study Notes Generation Guidelines

### Comprehensive Blog-Style Notes Requirements

When generating study notes, create a **comprehensive substitute for watching the video** that follows these requirements:

#### Content Depth & Structure
- **Full blog format**: Complete paragraphs, not bullet points or brief summaries
- **Comprehensive coverage**: Include all key concepts, examples, and speaker insights
- **Context preservation**: Maintain speaker's expertise, background, and credibility
- **Complete narrative**: Someone should understand the full content without watching

#### Note Organization Strategy
- **Identify video type first**: Technical deep-dive, methodology/framework, business strategy, etc.
- **Extract learning objectives**: What is the speaker trying to teach? What problem does this solve?
- **Capture specific insights**: Real examples, case studies, concrete numbers/metrics
- **Include anti-patterns**: What NOT to do is often more valuable than best practices

#### Content Requirements
- **Speaker expertise**: Include background, companies, years of experience, specific domain knowledge
- **Concrete examples**: All case studies, client stories, real-world implementations mentioned
- **Quantified impact**: Specific numbers, percentages, failure rates, improvement metrics
- **Actionable takeaways**: Implementation frameworks, step-by-step processes, practical next steps
- **Technical depth**: Specific tools, methodologies, architecture patterns, code examples

#### Quality Standards
- **Complete narrative flow**: Each section builds logically on the previous
- **Rich context**: Explain why concepts matter, not just what they are
- **Industry relevance**: Position insights within broader field/industry context  
- **Future application**: How readers can immediately apply these learnings

### Template Structure for Different Video Types

#### Technical Deep-Dive Videos
```markdown
# [Specific Technical Topic]: [Unique Value Proposition]
**Speaker:** Full name, title, company, years of experience
**Context:** Why this talk matters in the current technical landscape

## The Problem This Solves
[Comprehensive explanation of the challenge being addressed]

## [Speaker's Name]'s Approach: [Specific Methodology Name]
[Full explanation of their unique approach/framework]

## [Number] Key Technical Insights

### 1. [Specific Technical Concept]
[Full paragraph explanation with context]
**Real-world example:** [Specific case study or implementation]
**Technical implementation:** [How to actually do this]
**Common pitfalls:** [What goes wrong and why]

[Continue for all major insights...]

## Implementation Framework
[Step-by-step actionable process]

## Tools & Technologies Mentioned
[Specific recommendations with context for when to use each]

## Measuring Success
[Specific metrics and KPIs mentioned by speaker]

## Advanced Considerations
[Edge cases, scaling challenges, enterprise concerns]
```

#### Methodology/Framework Videos  
```markdown
# [Framework Name]: [Speaker's] Complete Guide to [Domain]
**Speaker credentials and why you should listen**

## The [Framework Name] Revolution
[Full context of why this approach emerged and what it replaces]

## [Number] Core Principles of [Framework Name]

### Principle 1: [Specific Principle Name]
[Complete explanation with real examples]
**Case study:** [Specific implementation story]
**Implementation in practice:** [Concrete steps]
**Success metrics:** [How to measure effectiveness]

[Continue for all principles...]

## Complete Implementation Guide
[Detailed step-by-step process with decision points]

## Common Implementation Challenges
[Real obstacles and how to overcome them]

## Scaling [Framework Name]
[Enterprise considerations and team adoption strategies]
```

## Integration with Workflow

This script handles steps 1-6 of the manual workflow:
- ✅ Extract transcript
- ✅ Clean transcript  
- ✅ Download video
- ✅ Auto-detect frame timestamps
- ✅ Extract frames
- ✅ Organize files

**Critical Next Step: Comprehensive Study Notes**
- Read the entire cleaned transcript thoroughly
- Identify the video type and speaker expertise
- Create comprehensive blog-style notes following the guidelines above
- Ensure notes serve as complete substitute for video viewing
- Include all specific examples, metrics, and implementation details
