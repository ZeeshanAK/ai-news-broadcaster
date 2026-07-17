import { useState, useRef, useEffect } from "react";
import {
  Sun, Cloud, Moon, Play, Pause, SkipBack, Volume2,
  ChevronLeft, Settings, Radio, Mic, Clock, Calendar,
  ChevronRight, Check, UserPlus, LogIn,
} from "lucide-react";

// ─── Types ───────────────────────────────────────────────────────────────────

type Slot = "morning" | "noon" | "evening";
type View = "dashboard" | "article" | "settings" | "auth";

interface BroadcastItem {
  id: string;
  slot: Slot;
  date: string;
  title: string;
  summary: string;
  fullText: string;
  duration: string;
  readTime: number;
}

interface UserPrefs {
  name: string;
  mobile: string;
  slots: { morning: boolean; noon: boolean; evening: boolean };
  times: { morning: number; noon: number; evening: number };
}

// ─── Slot config ─────────────────────────────────────────────────────────────

const SLOT_META: Record<Slot, {
  label: string;
  Icon: typeof Sun;
  color: string;
  badge: string;
  dot: string;
  bar: string;
  hours: number[];
  defaultHour: number;
}> = {
  morning: {
    label: "Morning", Icon: Sun, color: "#2dd4bf",
    badge: "bg-teal-400/10 text-teal-300", dot: "bg-teal-400", bar: "bg-teal-400",
    hours: [6, 7, 8, 9], defaultHour: 7,
  },
  noon: {
    label: "Noon", Icon: Cloud, color: "#60a5fa",
    badge: "bg-blue-400/10 text-blue-300", dot: "bg-blue-400", bar: "bg-blue-400",
    hours: [12, 13, 14, 15], defaultHour: 12,
  },
  evening: {
    label: "Evening", Icon: Moon, color: "#a78bfa",
    badge: "bg-violet-400/10 text-violet-300", dot: "bg-violet-400", bar: "bg-violet-400",
    hours: [19, 20, 21, 22], defaultHour: 20,
  },
};

const SLOTS: Slot[] = ["morning", "noon", "evening"];

const DAY_LABELS: Record<string, string> = {
  "2026-07-17": "Today",
  "2026-07-16": "Yesterday",
  "2026-07-15": "Jul 15",
  "2026-07-14": "Jul 14",
};

// ─── Data ────────────────────────────────────────────────────────────────────

const BROADCASTS: BroadcastItem[] = [
  {
    id: "t-m", slot: "morning", date: "2026-07-17",
    title: "OpenAI Unveils GPT-5 Turbo with Real-Time Reasoning",
    summary: "The latest model achieves unprecedented benchmark scores while slashing inference costs by 40%, signaling a new era of accessible superintelligence.",
    fullText: `OpenAI made waves this morning with the release of GPT-5 Turbo, a new model variant that pairs the raw capability of GPT-5 with dramatically reduced inference latency and cost. According to Sam Altman's announcement post, the model achieves a 94.2 on the ARC-AGI benchmark — previously considered a ceiling for current-generation models — while running at speeds comparable to GPT-4o mini.\n\nThe cost reduction is particularly significant: API pricing drops to $0.10 per million input tokens, making enterprise-scale deployment viable for thousands of organizations that previously found the economics prohibitive. Early access customers including Bloomberg, Salesforce, and Palantir confirmed the performance claims in their own internal evaluations.\n\nPerhaps most striking is the model's new "deliberate mode," which allows it to allocate additional compute on particularly complex problems without requiring developers to configure chain-of-thought prompting manually. The system detects problem complexity in real time and scales reasoning depth accordingly.\n\nAnalysts at Bernstein raised their OpenAI valuation estimate by 15% within hours of the announcement, noting that the cost-performance improvement could accelerate the timeline for AGI-adjacent commercial products from the company's portfolio companies.`,
    duration: "4:32", readTime: 3,
  },
  {
    id: "t-n", slot: "noon", date: "2026-07-17",
    title: "EU AI Act Enforcement Body Issues First Fines",
    summary: "Three major tech firms face combined penalties of €2.1 billion in the first enforcement actions under the landmark regulation, setting precedent for global AI governance.",
    fullText: `The European AI Office issued its first wave of enforcement actions under the EU AI Act today, levying fines totaling €2.1 billion against three unnamed multinational technology companies for violations in high-risk AI system categories.\n\nThe Office's chief enforcement officer, Dr. Aigerim Bekova, stated in a press briefing that the fines represent "a clear signal that the grace period is over." The largest single fine, €980 million, was issued for an AI recruitment system found to have disparate impact across protected characteristics without the required human oversight documentation.\n\nIndustry groups reacted sharply, with TechEurope calling the fines "disproportionate and chilling to innovation." Meanwhile, civil society organizations praised the enforcement as overdue.\n\nLegal experts note the fines will trigger appeals that could take years to resolve, but the EU's enforcement posture is expected to accelerate compliance timelines globally.`,
    duration: "5:14", readTime: 4,
  },
  {
    id: "t-e", slot: "evening", date: "2026-07-17",
    title: "Anthropic's Claude 4 Opus Sets New Coding Benchmark Record",
    summary: "An unprecedented 96.3% on SWE-bench Verified positions Claude 4 Opus as the dominant model for autonomous software engineering tasks.",
    fullText: `Anthropic released Claude 4 Opus this evening, immediately setting a new state-of-the-art on the SWE-bench Verified benchmark with a score of 96.3% — surpassing the previous best of 91.8% held by OpenAI's o3 model.\n\nThe model's architecture includes a new "agentic core" that maintains longer coherent action sequences, enabling it to navigate complex multi-file codebases without the context drift that has plagued previous generation models. Anthropic CTO Tom Brown described it as the model that "finally crosses the threshold where you can trust it with a pull request, not just a function."\n\nClaude.ai enterprise customers will gain access starting next week, with the API available to all developers in two weeks. Pricing is set at $15 per million input tokens and $75 per million output tokens.\n\nThe release sent competitor stocks lower in after-hours trading, with Alphabet down 2.3% and Microsoft off 1.8%. Shares of Anthropic's private market valuation jumped an estimated 22% according to Forge Global data.`,
    duration: "6:01", readTime: 4,
  },
  {
    id: "y-m", slot: "morning", date: "2026-07-16",
    title: "Google DeepMind Achieves Protein Structure Prediction Breakthrough",
    summary: "AlphaFold 4 predicts dynamic protein conformations in real time, opening new frontiers in drug discovery and personalized medicine.",
    fullText: `Google DeepMind announced AlphaFold 4, extending the landmark protein structure prediction system to handle dynamic conformational changes — the flexible, motion-based behavior of proteins that determines much of their biological function.\n\nPrevious AlphaFold versions could predict a protein's static structure with extraordinary accuracy, but the dynamic behavior remained largely out of reach. AlphaFold 4 predicts full conformational ensembles, effectively modeling how a protein moves and shifts as it performs its biological role.\n\nThe implications for drug discovery are immediate and significant. Early trials with two major pharmaceutical partners suggest a 3–5x reduction in lead optimization time for several therapeutic areas.`,
    duration: "3:45", readTime: 3,
  },
  {
    id: "y-n", slot: "noon", date: "2026-07-16",
    title: "Microsoft Copilot Surpasses 500 Million Monthly Active Users",
    summary: "The milestone cements AI assistants as mass-market productivity tools, with enterprise adoption driving over 60% of usage.",
    fullText: `Microsoft's Satya Nadella announced that Copilot has crossed 500 million monthly active users, a milestone that places it among the fastest-growing software products in history.\n\nEnterprise customers account for approximately 310 million of those users, reflecting deep penetration into corporate workflows since the product's general availability in late 2024. Word, Excel, and Teams remain the highest-engagement surfaces, with Copilot-assisted document drafting growing 340% year-over-year.\n\nThe announcement coincided with Microsoft's Q4 earnings call, where the company reported that AI services now contribute 23% of total revenue — up from 8% just eighteen months ago.`,
    duration: "4:08", readTime: 3,
  },
  {
    id: "y-e", slot: "evening", date: "2026-07-16",
    title: "xAI Grok 3 Released with 2M Token Context Window",
    summary: "Elon Musk's AI lab ships its most capable model yet, featuring a context window large enough to ingest entire codebases or book libraries in a single prompt.",
    fullText: `xAI released Grok 3 this evening, featuring a 2-million token context window that Elon Musk described on X as "basically infinite for any practical purpose." The model is available to X Premium+ subscribers immediately.\n\nThe context window milestone allows Grok 3 to process approximately 1,500 average-length novels or an entire large codebase in a single prompt — capabilities with significant implications for legal document analysis, software engineering, and academic research.\n\nIn benchmark testing published by xAI, Grok 3 scores competitively with GPT-5 Turbo on standard reasoning tasks while showing a particular edge on tasks requiring synthesis across large document sets.`,
    duration: "3:55", readTime: 3,
  },
  {
    id: "d2-m", slot: "morning", date: "2026-07-15",
    title: "NVIDIA Announces Blackwell Ultra GPU Architecture",
    summary: "The next-generation chip delivers 4x the training throughput of H100 while consuming 30% less power, reshaping the economics of large-scale AI training.",
    fullText: `NVIDIA CEO Jensen Huang unveiled the Blackwell Ultra GPU architecture at GTC 2026, promising a 4x improvement in training throughput over the current H100 generation with a 30% reduction in power consumption per FLOP.\n\nThe new architecture introduces a redesigned memory subsystem with 192GB of HBM4 per GPU and a new NVLink 6 interconnect allowing 128-GPU clusters to communicate at 9.6 TB/s aggregate bandwidth.\n\nShipments are expected to begin in Q4 2026, with cloud providers AWS, Google, and Azure already securing priority allocation. Analyst estimates suggest the Blackwell Ultra cycle could generate $120B in revenue for NVIDIA over 18 months.`,
    duration: "4:22", readTime: 3,
  },
  {
    id: "d2-n", slot: "noon", date: "2026-07-15",
    title: "Apple Intelligence Adds Real-Time Translation to All Apps",
    summary: "iOS 21's AI layer now translates any on-screen text or speech in real time, functioning as a universal interpreter embedded in the operating system.",
    fullText: `Apple released iOS 21 with a dramatically expanded Apple Intelligence feature set, headlined by a system-wide real-time translation capability that works across any application.\n\nThe feature uses a combination of on-device processing for common languages and a privacy-preserving cloud backend for less common language pairs. Apple's Private Cloud Compute infrastructure ensures that audio and text data is processed without being stored or associated with user accounts.\n\nFor businesses operating internationally, the implications are significant: the feature supports 94 languages at launch. Apple cited accessibility as a core motivation, noting that real-time translation removes language barriers for over 1.5 billion people.`,
    duration: "3:38", readTime: 3,
  },
  {
    id: "d2-e", slot: "evening", date: "2026-07-15",
    title: "Meta Releases Open-Source Llama 4 Scout Weights",
    summary: "The 17B parameter mixture-of-experts model outperforms Llama 3 70B on most benchmarks while running on consumer hardware, renewing the open-source AI movement.",
    fullText: `Meta released the weights for Llama 4 Scout — a 17 billion active parameter mixture-of-experts model — under a permissive open-source license, igniting immediate enthusiasm in the AI research and developer communities.\n\nRunning on a single RTX 4090, Llama 4 Scout achieves inference speeds of approximately 60 tokens per second. More significantly, its benchmark performance exceeds Llama 3 70B across 14 of 18 evaluated tasks.\n\nWithin six hours of release, the model had been downloaded over 2 million times from Hugging Face, and community fine-tunes began appearing within hours.`,
    duration: "5:02", readTime: 4,
  },
  {
    id: "d3-m", slot: "morning", date: "2026-07-14",
    title: "AI Agents Complete First Autonomous Scientific Discovery",
    summary: "A multi-agent system at Carnegie Mellon independently identified a novel catalyst for CO₂ conversion, with no human guidance beyond the initial research question.",
    fullText: `Researchers at Carnegie Mellon University published results showing that an autonomous AI agent system independently discovered a novel catalyst that converts CO₂ to methanol with 23% greater efficiency than current best-in-class materials.\n\nThe agent autonomously planned experiments, queried scientific literature, designed computational simulations, and synthesized conclusions over a 72-hour continuous run. The discovery has been submitted to Nature Chemistry and is currently under peer review.\n\nPrincipal investigator Prof. Yuki Tanaka described the result as "the moment the paradigm actually shifted, not just in rhetoric."`,
    duration: "4:48", readTime: 4,
  },
  {
    id: "d3-n", slot: "noon", date: "2026-07-14",
    title: "Perplexity AI Raises $1B at $20B Valuation",
    summary: "The AI search company's rapid revenue growth and enterprise momentum attracted a consortium of sovereign wealth funds and strategic investors.",
    fullText: `Perplexity AI closed a $1 billion funding round at a $20 billion valuation, led by a consortium including the Abu Dhabi sovereign wealth fund Mubadala, SoftBank Vision Fund 3, and Nvidia's venture arm.\n\nThe company disclosed for the first time that annual recurring revenue has reached $850 million, up from $100 million eighteen months ago. Perplexity Pro subscriptions now number 45 million globally.\n\nCEO Aravind Srinivas indicated the funding will accelerate expansion into financial services and healthcare verticals.`,
    duration: "3:28", readTime: 3,
  },
  {
    id: "d3-e", slot: "evening", date: "2026-07-14",
    title: "AI Video Generation Reaches Broadcast Quality",
    summary: "Runway's Gen-4 model produces 4K footage indistinguishable from professional camera work in blind tests, triggering urgent conversations about media authenticity.",
    fullText: `Runway released Gen-4, an AI video generation model that produced output rated as "indistinguishable from professional camera footage" by 73% of participants in a blind study conducted with film industry professionals.\n\nThe release immediately sparked debate across the media industry. The Directors Guild of America issued a statement calling for mandatory provenance labeling on AI-generated video distributed online. The AP and Reuters both announced updates to their verification protocols.\n\nRunway simultaneously released Vid-Detect, capable of identifying Gen-4 output with 89% accuracy.`,
    duration: "5:30", readTime: 4,
  },
];

const DAYS = ["2026-07-17", "2026-07-16", "2026-07-15", "2026-07-14"];

// ─── Helpers ─────────────────────────────────────────────────────────────────

function getBroadcast(date: string, slot: Slot) {
  return BROADCASTS.find((b) => b.date === date && b.slot === slot);
}

function formatHour(h: number) {
  if (h === 0) return "12 AM";
  if (h < 12) return `${h} AM`;
  if (h === 12) return "12 PM";
  return `${h - 12} PM`;
}

function parseDuration(d: string) {
  const [m, s] = d.split(":").map(Number);
  return m * 60 + s;
}

function formatTime(s: number) {
  const m = Math.floor(s / 60);
  const sec = s % 60;
  return `${m}:${String(sec).padStart(2, "0")}`;
}

// ─── Audio Player ─────────────────────────────────────────────────────────────

function AudioPlayer({ item }: { item: BroadcastItem }) {
  const [playing, setPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [volume, setVolume] = useState(0.8);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const { color, bar } = SLOT_META[item.slot];

  useEffect(() => {
    if (playing) {
      intervalRef.current = setInterval(() => {
        setProgress((p) => {
          if (p >= 100) { setPlaying(false); return 0; }
          return p + 0.3;
        });
      }, 100);
    } else {
      if (intervalRef.current) clearInterval(intervalRef.current);
    }
    return () => { if (intervalRef.current) clearInterval(intervalRef.current); };
  }, [playing]);

  const elapsed = Math.floor((progress / 100) * parseDuration(item.duration));

  // Static waveform heights derived from index — no random per render
  const waveHeights = Array.from({ length: 48 }, (_, i) =>
    6 + Math.abs(Math.sin(i * 0.9) * 6 + Math.sin(i * 2.1) * 4)
  );

  return (
    <div className="rounded-xl p-5 border border-border bg-secondary">
      <div className="flex items-end gap-[3px] h-10 mb-5">
        {waveHeights.map((h, i) => {
          const filled = (i / 48) * 100 <= progress;
          return (
            <div
              key={i}
              className="rounded-full flex-1 transition-all duration-150"
              style={{ height: `${h + 4}px`, background: filled ? color : "rgba(45,212,191,0.1)" }}
            />
          );
        })}
      </div>

      <div
        className="h-1 rounded-full mb-4 cursor-pointer"
        style={{ background: "rgba(45,212,191,0.1)" }}
        onClick={(e) => {
          const rect = e.currentTarget.getBoundingClientRect();
          setProgress(((e.clientX - rect.left) / rect.width) * 100);
        }}
      >
        <div className={`h-full rounded-full transition-all ${bar}`} style={{ width: `${progress}%` }} />
      </div>

      <div className="flex items-center justify-between mb-4 text-xs text-muted-foreground font-mono">
        <span>{formatTime(elapsed)}</span>
        <span>{item.duration}</span>
      </div>

      <div className="flex items-center gap-4">
        <button onClick={() => setProgress(0)} className="p-2 text-muted-foreground hover:text-foreground transition-colors">
          <SkipBack size={18} />
        </button>
        <button
          onClick={() => setPlaying((p) => !p)}
          className="w-12 h-12 rounded-full flex items-center justify-center transition-all hover:scale-105 active:scale-95"
          style={{ background: color }}
        >
          {playing
            ? <Pause size={20} className="text-background" />
            : <Play size={20} className="text-background ml-0.5" />}
        </button>
        <div className="flex items-center gap-2 ml-auto">
          <Volume2 size={16} className="text-muted-foreground" />
          <input
            type="range" min={0} max={1} step={0.01} value={volume}
            onChange={(e) => setVolume(Number(e.target.value))}
            className="w-20 accent-primary h-1"
          />
        </div>
      </div>
    </div>
  );
}

// ─── Broadcast Card ──────────────────────────────────────────────────────────

function BroadcastCard({ item, onClick, size = "normal" }: {
  item: BroadcastItem;
  onClick: () => void;
  size?: "normal" | "large";
}) {
  const meta = SLOT_META[item.slot];
  const Icon = meta.Icon;
  return (
    <button
      onClick={onClick}
      className={`group text-left w-full rounded-xl border border-border bg-card hover:border-teal-400/20 transition-all duration-200 hover:bg-secondary ${size === "large" ? "p-6" : "p-4"}`}
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <span className={`inline-flex items-center gap-1.5 text-xs font-medium px-2.5 py-1 rounded-full ${meta.badge}`}>
          <Icon size={11} />
          {meta.label}
        </span>
        <span className="text-[11px] text-muted-foreground font-mono">{item.duration}</span>
      </div>
      <h3
        className={`font-normal text-foreground group-hover:text-primary transition-colors leading-snug mb-2 ${size === "large" ? "text-base" : "text-sm"}`}
        style={{ fontFamily: "'Instrument Serif', serif" }}
      >
        {item.title}
      </h3>
      <p className={`text-muted-foreground leading-relaxed ${size === "large" ? "text-sm" : "text-xs"} line-clamp-2`}>
        {item.summary}
      </p>
      <div className="mt-3 flex items-center gap-1 text-xs text-teal-400/60 opacity-0 group-hover:opacity-100 transition-opacity">
        <span>Read &amp; listen</span>
        <ChevronRight size={12} />
      </div>
    </button>
  );
}

// ─── Article View ─────────────────────────────────────────────────────────────

function ArticleView({ item, onBack }: { item: BroadcastItem; onBack: () => void }) {
  const meta = SLOT_META[item.slot];
  const Icon = meta.Icon;
  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-10 backdrop-blur-md bg-background/80 border-b border-border px-6 py-4 flex items-center justify-between">
        <button onClick={onBack} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors">
          <ChevronLeft size={16} /> Back
        </button>
        <div className="flex items-center gap-2 text-xs text-muted-foreground font-mono">
          <span className={`w-2 h-2 rounded-full ${meta.dot}`} />
          {DAY_LABELS[item.date]} · {meta.label}
        </div>
      </header>

      <div className="max-w-2xl mx-auto px-6 py-10">
        <span className={`inline-flex items-center gap-1.5 text-xs font-medium px-2.5 py-1 rounded-full mb-5 ${meta.badge}`}>
          <Icon size={11} /> {meta.label} Broadcast
        </span>

        <h1 className="text-3xl font-normal text-foreground leading-tight mb-4" style={{ fontFamily: "'Instrument Serif', serif" }}>
          {item.title}
        </h1>

        <div className="flex items-center gap-4 text-xs text-muted-foreground font-mono mb-6 pb-6 border-b border-border">
          <span className="flex items-center gap-1.5"><Clock size={12} />{item.readTime} min read</span>
          <span className="flex items-center gap-1.5"><Mic size={12} />{item.duration} audio</span>
          <span className="flex items-center gap-1.5"><Calendar size={12} />{item.date}</span>
        </div>

        <div
          className="rounded-lg p-4 mb-6 text-sm leading-relaxed border-l-2"
          style={{ borderColor: meta.color, background: `${meta.color}10`, color: "#b0ccc9" }}
        >
          {item.summary}
        </div>

        <div className="mb-8">
          <p className="text-xs text-muted-foreground uppercase tracking-widest font-mono mb-3">Audio Broadcast</p>
          <AudioPlayer item={item} />
        </div>

        <div>
          <p className="text-xs text-muted-foreground uppercase tracking-widest font-mono mb-4">Full Article</p>
          {item.fullText.split("\n\n").map((para, i) => (
            <p key={i} className="text-sm text-foreground/80 leading-7 mb-4">{para}</p>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── Auth View (Register / Sign In) ──────────────────────────────────────────

function AuthView({ onComplete, onBack }: {
  onComplete: (prefs: UserPrefs) => void;
  onBack: () => void;
}) {
  const [mode, setMode] = useState<"register" | "signin">("register");
  const [step, setStep] = useState(0);
  const [name, setName] = useState("");
  const [mobile, setMobile] = useState("");
  const [slots, setSlots] = useState({ morning: true, noon: true, evening: true });
  const [times, setTimes] = useState({ morning: 7, noon: 12, evening: 20 });

  function finish() {
    onComplete({ name, mobile, slots, times });
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="flex items-center justify-between mb-10">
          <button onClick={onBack} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors">
            <ChevronLeft size={16} /> Back
          </button>
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-md bg-primary flex items-center justify-center">
              <Radio size={13} className="text-primary-foreground" />
            </div>
            <span className="font-mono text-xs tracking-widest text-foreground uppercase">AI Signal</span>
          </div>
        </div>

        {/* Mode toggle */}
        <div className="flex rounded-lg bg-secondary border border-border p-1 mb-8">
          {(["register", "signin"] as const).map((m) => (
            <button
              key={m}
              onClick={() => { setMode(m); setStep(0); }}
              className={`flex-1 flex items-center justify-center gap-2 py-2 text-sm rounded-md transition-all ${mode === m ? "bg-card text-foreground shadow-sm" : "text-muted-foreground hover:text-foreground"}`}
            >
              {m === "register" ? <UserPlus size={14} /> : <LogIn size={14} />}
              {m === "register" ? "Register" : "Sign In"}
            </button>
          ))}
        </div>

        {/* Sign In (simple) */}
        {mode === "signin" && (
          <div>
            <h2 className="text-2xl font-normal mb-1" style={{ fontFamily: "'Instrument Serif', serif" }}>
              Welcome back
            </h2>
            <p className="text-sm text-muted-foreground mb-6">Enter your mobile number to continue.</p>
            <div className="mb-6">
              <label className="text-xs text-muted-foreground block mb-1">Mobile number</label>
              <input
                type="tel" placeholder="+1 (555) 000-0000" value={mobile}
                onChange={(e) => setMobile(e.target.value)}
                className="w-full bg-secondary border border-border rounded-lg px-4 py-3 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
            <button
              disabled={!mobile}
              onClick={finish}
              className="w-full py-3 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-40"
            >
              Send verification code
            </button>
          </div>
        )}

        {/* Register — Step 0: name + mobile */}
        {mode === "register" && step === 0 && (
          <div>
            <h2 className="text-2xl font-normal mb-1" style={{ fontFamily: "'Instrument Serif', serif" }}>
              Create your account
            </h2>
            <p className="text-sm text-muted-foreground mb-6">Start receiving your daily AI intelligence brief.</p>
            <div className="space-y-3 mb-6">
              <div>
                <label className="text-xs text-muted-foreground block mb-1">Full name</label>
                <input
                  type="text" placeholder="Alex Chen" value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-secondary border border-border rounded-lg px-4 py-3 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>
              <div>
                <label className="text-xs text-muted-foreground block mb-1">Mobile number</label>
                <input
                  type="tel" placeholder="+1 (555) 000-0000" value={mobile}
                  onChange={(e) => setMobile(e.target.value)}
                  className="w-full bg-secondary border border-border rounded-lg px-4 py-3 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>
            </div>
            <button
              disabled={!name || !mobile}
              onClick={() => setStep(1)}
              className="w-full py-3 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-40"
            >
              Continue
            </button>
          </div>
        )}

        {/* Register — Step 1: broadcast schedule */}
        {mode === "register" && step === 1 && (
          <div>
            <h2 className="text-2xl font-normal mb-1" style={{ fontFamily: "'Instrument Serif', serif" }}>
              Set your broadcast schedule
            </h2>
            <p className="text-sm text-muted-foreground mb-6">
              Choose which broadcasts you receive and pick your preferred delivery hour.
            </p>

            <div className="space-y-4 mb-8">
              {SLOTS.map((slot) => {
                const meta = SLOT_META[slot];
                const Icon = meta.Icon;
                const on = slots[slot];
                return (
                  <div key={slot} className={`rounded-xl border p-5 transition-all ${on ? "border-teal-400/20 bg-card" : "border-border bg-transparent"}`}>
                    {/* Slot header with toggle */}
                    <div className="flex items-center justify-between mb-0">
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-lg flex items-center justify-center" style={{ background: `${meta.color}15` }}>
                          <Icon size={16} style={{ color: meta.color }} />
                        </div>
                        <div>
                          <div className="text-sm font-medium">{meta.label}</div>
                          <div className="text-xs text-muted-foreground font-mono">
                            {meta.hours[0]}:00 – {meta.hours[meta.hours.length - 1]}:00
                          </div>
                        </div>
                      </div>
                      {/* Toggle */}
                      <button
                        onClick={() => setSlots((s) => ({ ...s, [slot]: !s[slot] }))}
                        className={`w-11 h-6 rounded-full transition-colors relative flex-shrink-0 ${on ? "bg-primary" : "bg-muted"}`}
                      >
                        <span className={`absolute top-0.5 w-5 h-5 rounded-full bg-white shadow transition-all ${on ? "left-[22px]" : "left-0.5"}`} />
                      </button>
                    </div>

                    {/* Hour selector */}
                    {on && (
                      <div className="mt-4">
                        <p className="text-xs text-muted-foreground mb-2">Deliver at</p>
                        <div className="flex gap-2">
                          {meta.hours.map((h) => {
                            const selected = times[slot] === h;
                            return (
                              <button
                                key={h}
                                onClick={() => setTimes((t) => ({ ...t, [slot]: h }))}
                                className={`flex-1 py-2 rounded-lg text-xs font-mono transition-all border ${
                                  selected
                                    ? "border-primary bg-primary text-primary-foreground"
                                    : "border-border bg-secondary text-muted-foreground hover:text-foreground hover:border-teal-400/30"
                                }`}
                              >
                                {formatHour(h)}
                              </button>
                            );
                          })}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            <div className="flex gap-3">
              <button onClick={() => setStep(0)} className="flex-1 py-3 rounded-lg border border-border text-sm hover:bg-secondary transition-colors">
                Back
              </button>
              <button
                disabled={!Object.values(slots).some(Boolean)}
                onClick={finish}
                className="flex-1 py-3 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-40"
              >
                Start receiving broadcasts
              </button>
            </div>
          </div>
        )}

        {/* Step dots (register only) */}
        {mode === "register" && (
          <div className="flex gap-2 mt-8 justify-center">
            {[0, 1].map((i) => (
              <div key={i} className={`h-1 rounded-full transition-all ${i === step ? "w-6 bg-primary" : "w-2 bg-muted"}`} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Settings View ────────────────────────────────────────────────────────────

function SettingsView({ prefs, onChange, onBack }: {
  prefs: UserPrefs;
  onChange: (p: UserPrefs) => void;
  onBack: () => void;
}) {
  const [local, setLocal] = useState<UserPrefs>(prefs);

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-10 backdrop-blur-md bg-background/80 border-b border-border px-6 py-4 flex items-center justify-between">
        <button onClick={onBack} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors">
          <ChevronLeft size={16} /> Back
        </button>
        <button
          onClick={() => { onChange(local); onBack(); }}
          className="text-sm font-medium bg-primary text-primary-foreground px-4 py-1.5 rounded-lg hover:opacity-90 transition-opacity"
        >
          Save
        </button>
      </header>

      <div className="max-w-lg mx-auto px-6 py-10">
        <h1 className="text-2xl font-normal mb-1" style={{ fontFamily: "'Instrument Serif', serif" }}>
          Broadcast Settings
        </h1>
        <p className="text-sm text-muted-foreground mb-8">Manage your schedule and profile.</p>

        {/* Profile */}
        <section className="mb-8">
          <p className="text-xs text-muted-foreground uppercase tracking-widest font-mono mb-4">Profile</p>
          <div className="space-y-3">
            <div>
              <label className="text-xs text-muted-foreground block mb-1">Name</label>
              <input
                type="text" value={local.name}
                onChange={(e) => setLocal((p) => ({ ...p, name: e.target.value }))}
                className="w-full bg-secondary border border-border rounded-lg px-4 py-2.5 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
            <div>
              <label className="text-xs text-muted-foreground block mb-1">Mobile number</label>
              <input
                type="tel" value={local.mobile}
                onChange={(e) => setLocal((p) => ({ ...p, mobile: e.target.value }))}
                className="w-full bg-secondary border border-border rounded-lg px-4 py-2.5 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
          </div>
        </section>

        {/* Schedule */}
        <section>
          <p className="text-xs text-muted-foreground uppercase tracking-widest font-mono mb-4">Broadcast Schedule</p>
          <div className="space-y-4">
            {SLOTS.map((slot) => {
              const meta = SLOT_META[slot];
              const Icon = meta.Icon;
              const on = local.slots[slot];
              return (
                <div key={slot} className="rounded-xl border border-border bg-card p-5">
                  <div className="flex items-center justify-between mb-0">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ background: `${meta.color}15` }}>
                        <Icon size={15} style={{ color: meta.color }} />
                      </div>
                      <span className="font-medium text-sm">{meta.label}</span>
                    </div>
                    <button
                      onClick={() => setLocal((p) => ({ ...p, slots: { ...p.slots, [slot]: !p.slots[slot] } }))}
                      className={`w-11 h-6 rounded-full transition-colors relative ${on ? "bg-primary" : "bg-muted"}`}
                    >
                      <span className={`absolute top-0.5 w-5 h-5 rounded-full bg-white shadow transition-all ${on ? "left-[22px]" : "left-0.5"}`} />
                    </button>
                  </div>
                  {on && (
                    <div className="mt-4">
                      <p className="text-xs text-muted-foreground mb-2">Deliver at</p>
                      <div className="flex gap-2">
                        {meta.hours.map((h) => {
                          const selected = local.times[slot] === h;
                          return (
                            <button
                              key={h}
                              onClick={() => setLocal((p) => ({ ...p, times: { ...p.times, [slot]: h } }))}
                              className={`flex-1 py-2 rounded-lg text-xs font-mono transition-all border ${
                                selected
                                  ? "border-primary bg-primary text-primary-foreground"
                                  : "border-border bg-secondary text-muted-foreground hover:text-foreground hover:border-teal-400/30"
                              }`}
                            >
                              {formatHour(h)}
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>
      </div>
    </div>
  );
}

// ─── Dashboard ─────────────────────────────────────────────────────────────────

function Dashboard({ prefs, registered, onSelectArticle, onSettings, onRegister }: {
  prefs: UserPrefs | null;
  registered: boolean;
  onSelectArticle: (item: BroadcastItem) => void;
  onSettings: () => void;
  onRegister: () => void;
}) {
  const today = DAYS[0];
  const pastDays = DAYS.slice(1);
  const enabledSlots = registered && prefs
    ? SLOTS.filter((s) => prefs.slots[s])
    : SLOTS;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-10 backdrop-blur-md bg-background/80 border-b border-border px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
              <Radio size={15} className="text-primary-foreground" />
            </div>
            <span className="font-mono text-sm tracking-widest text-foreground uppercase hidden sm:block">AI Signal</span>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-xs text-muted-foreground font-mono hidden sm:block">
              {new Date().toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" })}
            </span>
            {registered ? (
              <button
                onClick={onSettings}
                className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-all"
              >
                <Settings size={16} />
              </button>
            ) : (
              <button
                onClick={onRegister}
                className="flex items-center gap-2 bg-primary text-primary-foreground text-sm font-medium px-4 py-2 rounded-lg hover:opacity-90 transition-opacity"
              >
                <UserPlus size={14} />
                Register
              </button>
            )}
          </div>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-6 py-8">
        {/* Guest banner */}
        {!registered && (
          <div className="mb-8 rounded-xl border border-teal-400/15 bg-teal-400/5 px-6 py-4 flex items-center justify-between gap-4">
            <div>
              <p className="text-sm text-foreground font-medium mb-0.5">Get broadcasts delivered to you</p>
              <p className="text-xs text-muted-foreground">Register to receive morning, noon, and evening AI news via SMS — with audio.</p>
            </div>
            <button
              onClick={onRegister}
              className="flex-shrink-0 flex items-center gap-1.5 text-sm text-primary hover:underline"
            >
              Get started <ChevronRight size={14} />
            </button>
          </div>
        )}

        {/* Today */}
        <section className="mb-12">
          <div className="flex items-baseline justify-between mb-6">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                <span className="text-xs font-mono text-muted-foreground uppercase tracking-widest">Live Today</span>
              </div>
              <h2 className="text-2xl text-foreground" style={{ fontFamily: "'Instrument Serif', serif" }}>
                Today&apos;s Broadcast
              </h2>
            </div>
            <span className="text-xs text-muted-foreground font-mono">{DAY_LABELS[today]}</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {enabledSlots.map((slot) => {
              const item = getBroadcast(today, slot);
              if (!item) return null;
              return <BroadcastCard key={slot} item={item} onClick={() => onSelectArticle(item)} size="large" />;
            })}
          </div>
        </section>

        {/* Past days */}
        <section>
          <h2 className="text-lg text-foreground mb-6" style={{ fontFamily: "'Instrument Serif', serif" }}>
            Past Broadcasts
          </h2>
          <div className="space-y-6">
            {pastDays.map((day) => (
              <div key={day}>
                <div className="flex items-center gap-3 mb-3">
                  <span className="text-xs font-mono text-muted-foreground">{DAY_LABELS[day]}</span>
                  <div className="flex-1 h-px bg-border" />
                  <span className="text-xs font-mono text-muted-foreground/40">{day}</span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  {enabledSlots.map((slot) => {
                    const item = getBroadcast(day, slot);
                    if (!item) return null;
                    return <BroadcastCard key={slot} item={item} onClick={() => onSelectArticle(item)} />;
                  })}
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

// ─── App Root ─────────────────────────────────────────────────────────────────

export default function App() {
  const [registered, setRegistered] = useState(false);
  const [prefs, setPrefs] = useState<UserPrefs | null>(null);
  const [view, setView] = useState<View>("dashboard");
  const [article, setArticle] = useState<BroadcastItem | null>(null);

  if (view === "auth") {
    return (
      <AuthView
        onComplete={(p) => { setPrefs(p); setRegistered(true); setView("dashboard"); }}
        onBack={() => setView("dashboard")}
      />
    );
  }

  if (view === "article" && article) {
    return <ArticleView item={article} onBack={() => setView("dashboard")} />;
  }

  if (view === "settings" && prefs) {
    return (
      <SettingsView
        prefs={prefs}
        onChange={setPrefs}
        onBack={() => setView("dashboard")}
      />
    );
  }

  return (
    <Dashboard
      prefs={prefs}
      registered={registered}
      onSelectArticle={(item) => { setArticle(item); setView("article"); }}
      onSettings={() => setView("settings")}
      onRegister={() => setView("auth")}
    />
  );
}
