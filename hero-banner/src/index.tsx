import { h, Fragment } from "preact"
import type {
  QuartzComponent,
  QuartzComponentConstructor,
  QuartzComponentProps,
} from "../../quartz/components/types"

const css = `
.hero-banner-container { width: 100%; margin-bottom: 2rem; }
.hero-banner-image { width: 100%; min-height: 200px; background-size: cover; background-position: center; border-radius: 12px; overflow: hidden; position: relative; display: flex; flex-direction: column; justify-content: flex-end; }
.hero-banner-overlay { padding: 1.5rem 1.2rem 1rem; background: linear-gradient(to top, rgba(0,0,0,.75), transparent); }
.hero-banner-overlay .article-title { color: #fff !important; margin: 0 0 .2rem !important; text-shadow: 0 2px 4px rgba(0,0,0,.4); }
.hero-banner-overlay .content-meta { margin: 0 !important; }
.hero-banner-overlay .content-meta, .hero-banner-overlay .content-meta time, .hero-banner-overlay .content-meta span { color: rgba(255,255,255,.9) !important; font-weight: 500; text-shadow: 0 1px 3px rgba(0,0,0,.5); }
`

function coverUrl(value: unknown): string | undefined {
  if (Array.isArray(value)) return coverUrl(value[0])
  const raw = value
  if (typeof raw !== "string" || raw.length === 0) return undefined
  const wikilink = raw.match(/^!?\[\[([^|\]]+)(?:\|[^\]]+)?\]\]$/)
  return wikilink?.[1] ?? raw
}

function assetUrl(cover: string, slug: string | undefined): string {
  if (/^(?:[a-z]+:|\/\/|\/)/i.test(cover)) return cover
  const path = cover
    .replace(/^\.\//, "")
    .split("/")
    .map((segment) => encodeURIComponent(segment.toLowerCase()))
    .join("/")
  const depth = slug?.split("/").filter(Boolean).length ?? 0
  return `${"../".repeat(Math.max(0, depth - 1))}${path}`
}

const HeroBanner: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  const title = String(fileData.frontmatter?.title ?? fileData.slug ?? "")
  const cover = coverUrl(
    fileData.frontmatter?.cover ??
      fileData.frontmatter?.socialImage ??
      fileData.frontmatter?.image ??
      (fileData as { socialImage?: unknown }).socialImage,
  )
  const date = fileData.dates?.modified ?? fileData.dates?.created
  const meta = date
    ? new Date(date).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "2-digit",
      })
    : ""
  const titleBlock = <h1 class="article-title">{title}</h1>
  const metaBlock = (
    <p class="content-meta">
      {meta && <time datetime={new Date(date!).toISOString()}>{meta}</time>}
    </p>
  )

  if (!cover)
    return (
      <Fragment>
        {titleBlock}
        {metaBlock}
      </Fragment>
    )
  return (
    <div class="hero-banner-container">
      <div
        class="hero-banner-image"
        style={{ backgroundImage: `url(${assetUrl(cover, fileData.slug)})` }}
        role="img"
        aria-label={title}
      >
        <div class="hero-banner-overlay">
          {titleBlock}
          {metaBlock}
        </div>
      </div>
    </div>
  )
}

HeroBanner.css = css
export default (() => HeroBanner) satisfies QuartzComponentConstructor
