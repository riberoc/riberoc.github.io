import { h, Fragment } from "preact"

function HeroBanner(props) {
  const { fileData } = props
  const cover = fileData.frontmatter?.cover
  const title = fileData.frontmatter?.title ?? fileData.filePath?.split("/").pop()
  const date = fileData.dates?.modified ?? fileData.dates?.created

  const titleBlock = h("h1", { class: "article-title" }, title)
  const metaBlock = h(
    "p",
    { class: "content-meta" },
    date ? h("time", null, new Date(date).toLocaleDateString()) : null,
  )

  if (cover) {
    return h(
      "div",
      { class: "hero-banner-container" },
      h(
        "div",
        { class: "hero-banner-image", style: { backgroundImage: `url(${cover})` } },
        h("div", { class: "hero-banner-overlay" }, titleBlock, metaBlock),
      ),
    )
  }

  return h(Fragment, null, titleBlock, metaBlock)
}

export default () => HeroBanner
