import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Global Food Shortages · One Step Back, Two Steps Forward · AKN24",
  description: "An AkashicOMNI v0.3.0 analysis of global food insecurity, its interacting causes, the leadership-awareness gap and practical pathways from protection to regeneration.",
};

const shell = { width: "min(1160px, calc(100% - 32px))", margin: "0 auto" };
const panel = {
  border: "1px solid rgba(216,185,92,.24)",
  borderRadius: 24,
  background: "linear-gradient(145deg, rgba(19,25,47,.94), rgba(8,12,28,.97))",
  boxShadow: "0 24px 80px rgba(0,0,0,.28)",
};

const metrics = [
  ["7.8%", "of the global population faced hunger in 2025", "SOFI 2026 global estimate; down from 8.1% in 2024, but progress was uneven."],
  ["≈345m", "people faced high levels of acute food insecurity", "GRFC 2026 estimate across assessed crisis contexts; not the same measure as chronic hunger."],
  ["318m", "people projected to face crisis-level hunger or worse in 2026", "WFP Global Outlook planning estimate, subject to changing conflict, climate and funding conditions."],
  ["133.3", "FAO Food Price Index in August 2026", "Up 1.9% from July and 2.5% year-on-year, while remaining 16.8% below the March 2022 peak."],
];

const evidence = [
  ["Established Evidence", "Conflict, economic shocks, weather extremes, displacement, disrupted trade and constrained humanitarian access are recurrent drivers of acute food insecurity. Food access, diet quality and stability matter alongside aggregate supply."],
  ["Interpretation", "A deficit of self-awareness and systems awareness among powerful decision-makers can worsen the crisis when short-term advantage, denial or narrow national and commercial incentives obscure downstream human consequences."],
  ["Lived Experience/Testimony", "Farmers, displaced communities, aid workers and food-insecure households experience the system from different positions. Their testimony can reveal mechanisms and harms that aggregate indicators miss, but it should not be universalised."],
  ["Hypothesis", "Leadership practices that combine reflective awareness, transparent evidence, affected-community participation and long-horizon consequence mapping may improve prevention and coordination."],
  ["Speculation", "A collective shift in consciousness could support a more compassionate food system. This is a moral and spiritual possibility, not a demonstrated causal intervention or substitute for policy, finance and logistics."],
];

const dimensions = [
  ["01", "AWAKEN", "Notice hunger without reducing it to a distant statistic."],
  ["02", "HIERATIC", "Treat food, soil and water as culturally meaningful relationships as well as resources."],
  ["03", "HOMESENSE", "Begin with kitchens, farms, markets and the lived reality of access."],
  ["04", "ADAPT", "Protect people now while adapting production, storage and distribution."],
  ["05", "REGENERATE", "Restore soils, watersheds, biodiversity and farmer agency where possible."],
  ["06", "TRANSCEND", "Move beyond zero-sum scarcity narratives toward shared planetary stewardship."],
  ["07", "#METAD v2.1", "Compare supply, access, nutrition, conflict, climate and governance explanations."],
  ["08", "ACTC v2.0", "Map actors, incentives, constraints, timing and causal pathways before assigning blame."],
  ["09", "MultidimensionalCUT v4.0.0 · PAST", "Trace colonial extraction, land concentration, conflict and earlier price shocks."],
  ["10", "MultidimensionalCUT v4.0.0 · PRESENT", "Separate chronic hunger, acute crisis and temporary market volatility."],
  ["11", "MultidimensionalCUT v4.0.0 · FUTURE", "Stress-test compounding climate, trade, energy and funding shocks."],
  ["12", "UMASC v7.2", "Relate material supply, human awareness, institutions, culture and ecology."],
  ["13", "AKASHICNET", "Hold the whole system together while preserving uncertainty and evidence boundaries."],
];

const sources = [
  ["The State of Food Security and Nutrition in the World 2026 · FAO", "https://www.fao.org/newsroom/detail/un-report--global-hunger-levels-ease-for-third-consecutive-year-but-progress-remains-uneven/en"],
  ["Global Report on Food Crises 2026 · FAO Open Knowledge", "https://openknowledge.fao.org/items/5af52c71-0c0f-4a76-83b7-4f9071111689"],
  ["Global Report on Food Crises 2026 · WFP", "https://www.wfp.org/publications/global-report-food-crises-grfc"],
  ["WFP 2026 Global Outlook", "https://www.wfp.org/publications/wfp-global-outlook"],
  ["FAO Food Price Index · August 2026", "https://www.fao.org/worldfoodsituation/foodpricesindex/en/"],
  ["Food Systems Countdown Report 2026 · FAO", "https://openknowledge.fao.org/handle/20.500.14283/ce0482en"],
  ["Food systems performance against targets · Nature Food (2026)", "https://www.nature.com/articles/s43016-026-01379-0"],
  ["Community gardens and urban food resilience · Discover Sustainability (2025)", "https://link.springer.com/article/10.1007/s43621-025-01628-5"],
  ["Community gardens and resilient cities · npj Urban Sustainability (2025)", "https://www.nature.com/articles/s42949-025-00272-2"],
  ["Community-supported agriculture evidence summary · County Health Rankings (2025)", "https://www.countyhealthrankings.org/strategies-and-solutions/what-works-for-health/strategies/community-supported-agriculture-csa"],
  ["Community food rescue and fridge model · Food Rescue US", "https://foodrescue.us/fridge-the-gap/"],
  ["Indigenous Peoples’ food systems · FAO", "https://www.fao.org/indigenous-peoples/our-pillars/fao-work-on-indigenous-food-systems/en"],
  ["Civil society and Indigenous Peoples’ agroecology input · FAO Open Knowledge (2026)", "https://openknowledge.fao.org/"],
];

export default function GlobalFoodShortagesReport() {
  return (
    <main style={{ minHeight: "100vh", color: "#f5f0e7", background: "radial-gradient(circle at 50% 8%, #17315a 0, #0a1026 34%, #050711 78%)" }}>
      <header className="nav-shell">
        <a className="wordmark" href="/" aria-label="AkashicNET.org home"><img className="brand-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt="" /><span className="brand-name">AKASHICNET.ORG</span></a>
        <nav aria-label="Page navigation"><a href="/">Home</a><a href="#situation">Situation</a><a href="#analysis">13D analysis</a><a href="#forward">Ways forward</a><a href="#evidence">Evidence</a><a href="#sources">Sources</a></nav>
      </header>

      <article>
        <section style={{ ...shell, padding: "clamp(70px,10vw,132px) 0 50px", textAlign: "center" }}>
          <p className="section-label">AKN24 · GLOBAL SYSTEMS DESK · 14 SEPTEMBER 2026</p>
          <h1 style={{ margin: "18px auto", maxWidth: 1080, fontSize: "clamp(3rem,7.5vw,7rem)", lineHeight: .94 }}>Global Food<br/><em style={{ color: "#d8b95c" }}>Shortages</em></h1>
          <p style={{ color: "#e7cd7e", fontWeight: 800, letterSpacing: ".08em" }}>ONE STEP BACK · TWO STEPS FORWARD</p>
          <p style={{ maxWidth: 880, margin: "24px auto 0", color: "#d7d9e4", fontSize: "clamp(1.1rem,2.2vw,1.42rem)", lineHeight: 1.75 }}>The world does not face one uniform shortage. It faces overlapping crises of hunger, affordability, access, nutrition and resilience. An AkashicOMNI v0.3.0 analysis of what is happening, why narrow awareness can deepen it and how foresight can become action.</p>
        </section>

        <figure style={{ ...shell, ...panel, overflow: "hidden", padding: 0 }}>
          <img src="/images/akn24-global-food-shortages.webp" alt="AKN24 editorial illustration showing drought, disrupted logistics and empty crates on one side of Earth, transitioning to gardens, healthy soil, rainwater collection, chickens, a goat and coastal aquaculture on the other." style={{ display: "block", width: "100%", height: "auto" }} />
          <figcaption style={{ padding: "16px 20px", color: "#b9bfd0", lineHeight: 1.65 }}><strong style={{ color: "#f3dc96" }}>From fragility to resilience.</strong> This is an AkashicNET editorial illustration, not documentary evidence, a forecast or a claim that household production can replace global food systems.</figcaption>
        </figure>

        <section id="situation" style={{ ...shell, padding: "78px 0 24px" }}>
          <p className="section-label">THE SITUATION</p>
          <h2 style={{ maxWidth: 920, fontSize: "clamp(2.2rem,5vw,4.5rem)", lineHeight: 1.04 }}>Improvement in one global measure can coexist with deepening crisis elsewhere.</h2>
          <p style={{ maxWidth: 900, color: "#d7d9e4", lineHeight: 1.85, fontSize: "1.08rem" }}>SOFI 2026 estimates that the global prevalence of hunger eased in 2025. GRFC and WFP figures still show hundreds of millions facing acute food insecurity in crisis-affected settings. These are not contradictions: the datasets answer different questions, cover different populations and use different thresholds.</p>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(235px,1fr))", gap: 16, marginTop: 28 }}>
            {metrics.map(([value,label,note]) => <article key={value} style={{ ...panel, padding: 24 }}><p style={{ color: "#e7cd7e", fontSize: "clamp(2rem,5vw,3.4rem)", fontWeight: 900, margin: 0 }}>{value}</p><h3 style={{ lineHeight: 1.35 }}>{label}</h3><p style={{ color: "#aeb5c6", lineHeight: 1.65, marginBottom: 0 }}>{note}</p></article>)}
          </div>
          <div style={{ ...panel, padding: "clamp(24px,4vw,42px)", marginTop: 18 }}>
            <h3 style={{ color: "#e7cd7e", fontSize: "1.5rem", marginTop: 0 }}>What “shortage” can mean</h3>
            <p style={{ color: "#d7d9e4", lineHeight: 1.8, marginBottom: 0 }}><strong>Availability:</strong> insufficient food in a place. <strong>Access:</strong> food exists but people cannot afford or safely reach it. <strong>Nutrition:</strong> calories are available but healthy diets are not. <strong>Stability:</strong> supply or access repeatedly fails under shock. A strong analysis asks which condition exists, where, for whom and for how long.</p>
          </div>
        </section>

        <section style={{ ...shell, padding: "70px 0 24px" }}>
          <p className="section-label">WHY THE SYSTEM BREAKS</p>
          <h2 style={{ fontSize: "clamp(2.2rem,5vw,4.4rem)", lineHeight: 1.04 }}>Pressure becomes crisis through interaction.</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(250px,1fr))", gap: 16, marginTop: 28 }}>
            {[
              ["Conflict and displacement", "War removes land and labour from production, damages storage and ports, blocks aid and destroys purchasing power."],
              ["Climate and ecological stress", "Heat, drought, floods, water scarcity, soil degradation and biodiversity loss make harvests and livelihoods less predictable."],
              ["Prices and inequality", "Inflation, poverty, debt and unequal bargaining power convert a market shock into hunger even when food remains available."],
              ["Concentrated logistics", "Dependence on a small number of exporters, routes, fuels, fertilisers and storage systems lets local disruption cascade."],
              ["Loss and waste", "Food lost between farm and market or wasted after purchase reduces effective supply while consuming land, energy and water."],
              ["Aid and governance constraints", "Late warning, political obstruction, funding gaps and weak accountability allow preventable deterioration."],
            ].map(([title,text]) => <article key={title} style={{ ...panel, padding: 24 }}><h3 style={{ color: "#e7cd7e", fontSize: "1.4rem" }}>{title}</h3><p style={{ color: "#cbd0dd", lineHeight: 1.72 }}>{text}</p></article>)}
          </div>
        </section>

        <section style={{ ...shell, padding: "70px 0 20px" }}>
          <div style={{ ...panel, padding: "clamp(28px,5vw,54px)", background: "radial-gradient(circle at 15% 10%,rgba(187,74,55,.18),rgba(9,13,31,.97) 58%)" }}>
            <p className="section-label">THE AWARENESS GAP</p>
            <h2 style={{ fontSize: "clamp(2.1rem,5vw,4.2rem)", marginTop: 12 }}>Are less-aware leaders part of the problem?</h2>
            <p style={{ color: "#d7d9e4", lineHeight: 1.85 }}>Potentially, but this is an <strong>interpretive systems claim</strong>, not a clinical judgement about particular people. Decisions become more harmful when leaders and institutions cannot or will not examine their assumptions, read social conditions, recognise the humanity of distant people or trace consequences across an interconnected system.</p>
            <p style={{ color: "#d7d9e4", lineHeight: 1.85 }}>Low awareness is not the sole cause. Structures matter: incentives, concentrated ownership, historical inequality, conflict, debt, infrastructure and ecological limits shape what leaders can see and do. Awareness without power or resources is insufficient; power without awareness is dangerous.</p>
            <blockquote style={{ color: "#f2d98e", fontSize: "clamp(1.3rem,2.8vw,2rem)", lineHeight: 1.45, margin: "28px 0 0" }}>“One step back to perceive the whole. Two steps forward through foresight and action.”</blockquote>
          </div>
        </section>

        <section id="analysis" style={{ ...shell, padding: "78px 0 22px" }}>
          <p className="section-label">AKASHICOMNI v0.3.0 · TRUE 13D ANALYSIS</p>
          <h2 style={{ maxWidth: 900, fontSize: "clamp(2.2rem,5vw,4.5rem)", lineHeight: 1.04 }}>Thirteen lenses. One food system.</h2>
          <figure style={{ ...panel, overflow: "hidden", padding: 0, marginTop: 30 }}>
            <img src="/images/akashicomni-global-food-security-13d.webp" alt="Conceptual AkashicOMNI circular map placing global food security at the centre of thirteen analytical lenses: AWAKEN, HIERATIC, HOMESENSE, ADAPT, REGENERATE, TRANSCEND, METAD, ACTC, past, present, future, UMASC and AkashicNET." style={{ display: "block", width: "100%", height: "auto" }} />
            <figcaption style={{ padding: "16px 20px", color: "#b9bfd0", lineHeight: 1.65 }}><strong style={{ color: "#f3dc96" }}>Analytical architecture.</strong> The image visualises a framework. It does not measure hunger, rank countries or establish causal effects.</figcaption>
          </figure>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(245px,1fr))", gap: 16, marginTop: 26 }}>
            {dimensions.map(([number,title,text]) => <article key={number} style={{ ...panel, padding: 22 }}><span style={{ color: "#d8b95c", fontWeight: 900 }}>{number}</span><h3 style={{ fontSize: "1.2rem", margin: "8px 0" }}>{title}</h3><p style={{ color: "#cbd0dd", lineHeight: 1.65, marginBottom: 0 }}>{text}</p></article>)}
          </div>
        </section>

        <section id="forward" style={{ ...shell, padding: "76px 0 22px" }}>
          <p className="section-label">TWO STEPS FORWARD</p>
          <h2 style={{ fontSize: "clamp(2.2rem,5vw,4.4rem)", lineHeight: 1.04 }}>Protection now. Regeneration next.</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(290px,1fr))", gap: 18, marginTop: 28 }}>
            <article style={{ ...panel, padding: "clamp(24px,4vw,42px)" }}><p className="section-label">STEP 1 · AWARENESS → FORESIGHT</p><h3 style={{ fontSize: "1.7rem" }}>See who is vulnerable before the system fails.</h3><ul style={{ color: "#cbd0dd", lineHeight: 1.8, paddingLeft: 22 }}><li>Use transparent early-warning, market, weather and nutrition data.</li><li>Listen to farmers, Indigenous and local knowledge holders, women, displaced people and aid workers.</li><li>Map second-order effects before export bans, subsidy changes or conflict decisions.</li><li>Pre-position finance, food and logistics before a forecast becomes famine.</li></ul></article>
            <article style={{ ...panel, padding: "clamp(24px,4vw,42px)" }}><p className="section-label">STEP 2 · FORESIGHT → ACTION</p><h3 style={{ fontSize: "1.7rem" }}>Turn understanding into resilient capacity.</h3><ul style={{ color: "#cbd0dd", lineHeight: 1.8, paddingLeft: 22 }}><li>Protect humanitarian corridors, school meals, cash support and maternal and child nutrition.</li><li>Diversify crops, trade partners, storage, energy and transport routes.</li><li>Restore soil and water systems and reduce loss and waste.</li><li>Align incentives with fair livelihoods, healthy diets and ecological resilience.</li></ul></article>
          </div>
        </section>

        <section style={{ ...shell, padding: "70px 0 22px" }}>
          <p className="section-label">A PRACTICAL RESILIENCE MODEL</p>
          <h2 style={{ maxWidth: 960, fontSize: "clamp(2.2rem,5vw,4.4rem)", lineHeight: 1.04 }}>Consume more consciously. Grow more locally. Share capacity.</h2>
          <p style={{ maxWidth: 920, color: "#d7d9e4", lineHeight: 1.85 }}>“Eating less” needs a precise ethical boundary. People experiencing hunger or malnutrition do not need to consume less. Where diets and purchasing patterns are excessive, however, reducing overconsumption, food waste and unnecessarily resource-intensive demand can release household money and reduce pressure on land, water, energy and supply chains.</p>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(250px,1fr))", gap: 16, marginTop: 28 }}>
            {[
              ["Waste less", "Plan portions, use leftovers, share surplus, improve storage and rescue safe food before it becomes waste."],
              ["Grow within cities", "Use allotments, balconies, rooftops, courtyards, school gardens, hydroponics and carefully managed vertical farms for suitable crops."],
              ["Build food co-ops", "Pool purchasing, storage, transport and member labour so healthy food and resilient infrastructure become more accessible."],
              ["Back local farmers", "Use farmers markets, community-supported agriculture, advance purchasing and fair contracts to give growers predictable demand and income."],
              ["Close local loops", "Connect food scraps to safe composting, rainwater to permitted irrigation, local production to community kitchens and seasonal surplus to preservation."],
              ["Share knowledge and tools", "Create seed libraries, tool libraries, growing workshops, communal freezers and neighbourhood response plans."],
            ].map(([title,text]) => <article key={title} style={{ ...panel, padding: 24 }}><h3 style={{ color: "#e7cd7e", fontSize: "1.4rem" }}>{title}</h3><p style={{ color: "#cbd0dd", lineHeight: 1.72 }}>{text}</p></article>)}
          </div>
          <div style={{ ...panel, padding: "clamp(24px,4vw,42px)", marginTop: 18, background: "radial-gradient(circle at 85% 10%,rgba(65,164,112,.18),rgba(9,13,31,.97) 58%)" }}>
            <h3 style={{ color: "#a7f0c1", fontSize: "1.55rem", marginTop: 0 }}>The self-sustaining community, reframed</h3>
            <p style={{ color: "#d7d9e4", lineHeight: 1.8 }}>Complete self-sufficiency is rarely realistic or desirable. A stronger goal is <strong>community food resilience</strong>: enough local growing, storage, skills, mutual aid and trusted producer relationships to absorb disruption, while remaining connected to regional and global networks for foods, tools and inputs that cannot be produced locally.</p>
            <p style={{ color: "#d7d9e4", lineHeight: 1.8, marginBottom: 0 }}><strong>Neighbourhood layer:</strong> gardens, kitchens, preservation and sharing. <strong>City-region layer:</strong> co-ops, markets, warehouses, composting and peri-urban farms. <strong>National and global layer:</strong> staple reserves, fair trade, energy, fertiliser, transport and humanitarian coordination. Resilience comes from overlapping layers, not isolation.</p>
          </div>
        </section>

        <section style={{ ...shell, padding: "70px 0 22px" }}>
          <p className="section-label">FROM PLANET TO PLATE</p>
          <h2 style={{ maxWidth: 920, fontSize: "clamp(2.2rem,5vw,4.4rem)", lineHeight: 1.04 }}>Resilience is practical, local and connected.</h2>
          <p style={{ maxWidth: 900, color: "#d7d9e4", lineHeight: 1.85 }}>An allotment, community garden or balcony can add vegetables and skills. Chickens may provide eggs and goats milk, but only where land, welfare knowledge, time and local rules permit. Rainwater capture, seed sharing, preserving, freezing, community kitchens and neighbourhood exchange can reduce fragility. None makes a household independent of land, feed, veterinary care, energy, tools or wider logistics.</p>
          <div style={{ ...panel, padding: "clamp(24px,4vw,42px)", marginTop: 24 }}>
            <h3 style={{ color: "#e7cd7e", fontSize: "1.55rem", marginTop: 0 }}>The pizza test 🍕</h3>
            <p style={{ color: "#d7d9e4", lineHeight: 1.8 }}>Eggs, goat cheese, spinach, broccoli and nearby salmon could cover a formidable keto breakfast and evening meal. But what would still arrive through the network? Salt, olive oil, coffee, cacao, spices, animal feed, medicines, spare parts and energy reveal the hidden dependencies. Proper Italian pizza may remain a logistical luxury. Pineapple is excluded on civilisational grounds, not food-security evidence. 🇮🇹</p>
          </div>
        </section>

        <section style={{ ...shell, padding: "72px 0 22px" }}>
          <p className="section-label">OPEN-WEB AND COMMUNITY SOLUTIONS SCAN</p>
          <h2 style={{ maxWidth: 960, fontSize: "clamp(2.2rem,5vw,4.4rem)", lineHeight: 1.04 }}>Promising alternatives, with their limits visible.</h2>
          <p style={{ maxWidth: 920, color: "#d7d9e4", lineHeight: 1.85 }}>A scan of research, public initiatives and community discourse found practical models worth testing. Social-media visibility is treated as discovery or testimony, not validation. AkashicNET and the indexed r/NeuronsToNirvana and r/TribalGathering material did not provide a sufficiently documented food-security programme to promote as evidence. The clearest relevant community theme was Tribal Gathering’s influence on AkashicNET through intercultural meeting, Indigenous knowledge, nature and community. That can inform process, but it does not establish agricultural effectiveness.</p>
          <div style={{ display: "grid", gap: 14, marginTop: 28 }}>
            {[
              ["Community gardens and allotments", "SUPPORTED FOR MULTIPLE BENEFITS", "Reviews associate participation with fresh-food access, knowledge, wellbeing, social connection and urban resilience. Output and benefits vary, land access is unequal and gardens cannot replace staple supply."],
              ["Subsidised CSA and farmer co-ops", "PROMISING WITH ACCESS SUPPORT", "Advance subscriptions and cooperative purchasing can stabilise farmer income and relationships. Subsidies, flexible payments and accessible collection are needed to avoid serving only higher-income households."],
              ["Community fridges and food rescue", "PRACTICAL NEAR-TERM BRIDGE", "Redistribution can connect safe surplus with people who need it while reducing waste. It requires reliable stewardship, refrigeration, food-safety rules and must not become a substitute for adequate income."],
              ["Indigenous-led food sovereignty", "RIGHTS-BASED SYSTEM CHANGE", "Locally governed food systems can preserve ecological knowledge, culture, biodiversity and self-determination. Work must be led by rights-holders with consent and benefit-sharing, not extract knowledge as a generic technique."],
              ["Rooftop, hydroponic and vertical growing", "CONTEXT-DEPENDENT SUPPLEMENT", "These approaches can shorten routes for herbs and perishable produce where land is scarce. Capital, energy, water, nutrient inputs, maintenance and crop limits determine whether they improve resilience."],
              ["Food forests and edible public space", "LOCAL EXPERIMENT", "Perennial planting can diversify neighbourhood food and ecological functions over time. Tenure, contamination testing, maintenance, harvesting rules and seasonal yield need local design."],
              ["Shared cold storage and processing", "HIGH-LEVERAGE INFRASTRUCTURE", "Cooperative freezers, cool rooms, drying, fermentation and canning facilities can extend local harvests and reduce loss. Energy reliability, training and safety governance are essential."],
              ["Open local food maps", "COORDINATION TOOL", "Public maps of growers, co-ops, kitchens, fridges, water, storage and transport can reveal gaps and coordinate response. Privacy, data quality and exclusion risks must be managed."],
            ].map(([title,status,text]) => <article key={title} style={{ ...panel, padding: "22px clamp(22px,4vw,42px)", display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(min(100%,235px),1fr))", gap: 22 }}><div><h3 style={{ margin: "0 0 8px", color: "#e7cd7e" }}>{title}</h3><span style={{ color: "#a7f0c1", fontWeight: 900, fontSize: ".82rem", letterSpacing: ".06em" }}>{status}</span></div><p style={{ margin: 0, color: "#cbd0dd", lineHeight: 1.72 }}>{text}</p></article>)}
          </div>
          <div style={{ ...panel, padding: "clamp(24px,4vw,42px)", marginTop: 18 }}>
            <h3 style={{ color: "#e7cd7e", fontSize: "1.55rem", marginTop: 0 }}>A realistic city-region prototype</h3>
            <p style={{ color: "#d7d9e4", lineHeight: 1.8, marginBottom: 0 }}>Link inner-city growing sites and school gardens to peri-urban farms; organise purchasing through resident-owned co-ops and subsidised CSA shares; route safe surplus through community fridges and kitchens; add shared cold storage, composting and preservation; publish an open resource map; and measure affordability, nutrition, farmer income, waste, energy use and who actually benefits. Expand only what survives independent evaluation.</p>
          </div>
        </section>

        <section id="evidence" style={{ ...shell, padding: "78px 0 22px" }}>
          <p className="section-label">EVIDENCE MAP</p>
          <h2 style={{ fontSize: "clamp(2.2rem,5vw,4.4rem)", lineHeight: 1.04 }}>Many pathways. Clear boundaries.</h2>
          <div style={{ display: "grid", gap: 14, marginTop: 30 }}>
            {evidence.map(([title,text],index) => <article key={title} style={{ ...panel, padding: "22px clamp(22px,4vw,42px)", display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(min(100%,240px),1fr))", gap: 22 }}><h3 style={{ margin: 0, color: ["#8de6ff","#8fcfff","#a7f0c1","#e7cd7e","#d9a6ff"][index] }}>{title}</h3><p style={{ margin: 0, color: "#cbd0dd", lineHeight: 1.72 }}>{text}</p></article>)}
          </div>
        </section>

        <section id="sources" style={{ ...shell, padding: "76px 0 24px" }}>
          <p className="section-label">SOURCES AND PROVENANCE</p>
          <h2 style={{ fontSize: "clamp(2.1rem,5vw,4rem)" }}>Follow the evidence trail.</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(250px,1fr))", gap: 14 }}>
            {sources.map(([title,href]) => <a key={href} href={href} style={{ ...panel, padding: 20, display: "block", color: "inherit", textDecoration: "none" }}><span style={{ color: "#d8b95c", fontWeight: 900 }}>SOURCE ↗</span><h3 style={{ lineHeight: 1.35 }}>{title}</h3></a>)}
          </div>
          <p style={{ color: "#9fa7ba", lineHeight: 1.75, marginTop: 22 }}><strong>Scope and exclusions.</strong> This report is a global systems overview, not a country forecast, dietary prescription or claim that spiritual practice prevents hunger. Figures use different definitions and denominators and should not be added together. The 2026 situation remains dynamic; publication dates, coverage and revisions should be checked at source.</p>
          <p style={{ color: "#9fa7ba", lineHeight: 1.75 }}><strong>Transparency.</strong> Primary factual direction: FAO, WFP, GRFC and Food Systems Countdown publications. Editorial synthesis: AkashicOMNI v0.3.0 and AkashicNET. Humorous household scenario: adapted from the originating conversation. AI assistance: research organisation, drafting, code and conceptual editorial artwork. Human review remains required before promotion.</p>
        </section>

        <section style={{ ...shell, padding: "70px 0 90px", textAlign: "center" }}>
          <p className="section-label">THE AKN24 GLOBAL SYSTEMS DESK</p>
          <h2 style={{ maxWidth: 940, margin: "16px auto", fontSize: "clamp(2.2rem,5vw,4.6rem)", lineHeight: 1.05 }}>Food security is not only about producing more. It is about perceiving more clearly, protecting more fairly and coordinating more wisely.</h2>
          <p style={{ color: "#e7cd7e", fontSize: "1.2rem" }}>Awareness → Foresight → Action</p>
          <p style={{ maxWidth: 720, margin: "32px auto 0", color: "#cbd0dd", lineHeight: 1.7 }}>If this independent report helped, support future open-access analyses with a suggested €13 contribution.</p>
          <a href="https://buymeacoffee.com/akashicnet" style={{ display: "inline-block", marginTop: 16, padding: "14px 22px", borderRadius: 999, background: "#d8b95c", color: "#090d1c", fontWeight: 900, textDecoration: "none" }}>☕ Support AkashicNET</a>
          <p style={{ color: "#9fa7ba" }}>Fund the question—not the answer.</p>
        </section>
      </article>
      <footer><div><img className="footer-symbol" src="/images/akashicnet-toroidal-love-logo.png" alt="" /><p className="brand-name">AKASHICNET.ORG</p></div><p>Unity through neurodiversity.</p><p>Awaken within · Serve without · 2026</p></footer>
    </main>
  );
}
