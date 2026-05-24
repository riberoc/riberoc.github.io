import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import ArticleTitle from "./ArticleTitle"
import ContentMeta from "./ContentMeta"

export default (() => {
  const HeroHeader: QuartzComponent = (props: QuartzComponentProps) => {
    const { fileData } = props
    const cover = fileData.frontmatter?.cover as string | undefined

    // Component configurations extracted from your layout properties
    const TitleComponent = ArticleTitle()
    const MetaComponent = ContentMeta()

    if (cover) {
      return (
        <div className="hero-banner-container">
          <div className="hero-banner-image" style={{ backgroundImage: `url(${cover})` }}>
            <div className="hero-banner-overlay">
              <TitleComponent {...props} />
              <MetaComponent {...props} />
            </div>
          </div>
        </div>
      )
    }

    // Standard Fallback when no cover metadata is specified
    return (
      <>
        <TitleComponent {...props} />
        <MetaComponent {...props} />
      </>
    )
  }

  return HeroHeader
}) satisfies QuartzComponentConstructor
