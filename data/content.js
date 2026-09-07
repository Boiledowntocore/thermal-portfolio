window.SITE = {
  person: {
    name: "Prince Chauhan",
    role: "Thermal engineer",
    location: "Bengaluru",
    email: "princechauhan92652@gmail.com",
    linkedin: "https://www.linkedin.com/in/prince-chauhan-470031166/",
    resume: "assets/Prince_Chauhan_Resume.pdf",
    lede: [
      "Liquid-cooled battery and charger systems holding multi-pack platforms in their window from −10 to 55 °C, at supercharge rates.",
      "That work is now moving toward <span class=\"mark\">spacecraft thermal control</span>."
    ],
    envelope: { low: "−10 °C", high: "+55 °C", span: "65 °C" }
  },

  projects: [
    {
      code: "TH-01",
      title: "Prawaas 4.0 supercharging demonstrator",
      sentence: "Held packs at 25–35 °C through a 110 kWh supercharge at peak-summer ambient — 100-plus swaps, no thermal fault.",
      role: "System architecture, validation",
      scale: "650 kg packs · 110 kWh · 50 °C",
      outcome: "100+ swaps, zero faults",
      year: "2024",
      figs: [
        { n: 1, src: "assets/media/prawaas-loop.svg", title: "Demonstrator coolant loop", caption: "Coolant loop with DAQ instrumentation" }
      ]
    },
    {
      code: "TH-02",
      title: "First-principles BTMS/CTMS architecture",
      sentence: "A coolant-loop architecture sized from heat-load first principles, where the supplied chiller measured well under its rated capacity.",
      role: "Thermal design, supplier validation",
      scale: "20–110 kWh · −10 to 55 °C",
      outcome: "~18% thermal-resistance cut",
      year: "2023–2025",
      figs: [
        { n: 2, src: "assets/media/architecture-loop.svg", title: "BTMS/CTMS architecture", caption: "Platform coolant-loop topology" },
        { n: 3, src: "assets/media/btms-capacity.svg", title: "Chiller capacity", caption: "Measured vs rated, normalised" }
      ]
    },
    {
      code: "TH-03",
      title: "Charger power-electronics cooling",
      sentence: "A redundant-pump liquid loop for the charger rectifier stage; on test it derated faster above 50 °C than datasheet allowed.",
      role: "Loop sizing, vendor qualification",
      scale: "Multi-pack charging station",
      outcome: "Derating fed back to supplier",
      year: "2024–2025",
      figs: [
        { n: 4, src: "assets/media/ctms-loop.svg", title: "Charger cooling loop", caption: "Redundant-pump liquid loop" },
        { n: 5, src: "assets/media/rectifier-derating.svg", title: "Rectifier derating", caption: "Measured vs datasheet, normalised" }
      ]
    },
    {
      code: "TH-04",
      title: "Thermal SOR & ECU control logic",
      sentence: "The governing spec and a four-mode control scheme, verified against an ECU simulator before hardware.",
      role: "Spec owner, simulator author",
      scale: "BTMS + CTMS · CAN 2.0",
      outcome: "Pre-hardware fault detection",
      year: "2024",
      figs: [
        { n: 6, src: "assets/media/sor-states.svg", title: "Operating-mode state machine", caption: "Four modes plus fault state" }
      ]
    }
  ],

  earlier: [
    { title: "Formula Bharat chassis optimisation", clause: "National win, chassis FEA, 15% mass cut", year: "2018–2022" },
    { title: "3 kW solar-tree system", clause: "~50% cost, ~80% footprint vs fixed array", year: "2022–2023" }
  ],

  // Straight from the résumé. There is no 2022–23 employment row: the solar-tree
  // build was an independent project and is listed under Earlier, not here.
  experience: [
    { year: "2023–present", role: "Thermal systems engineer", org: "SUN Mobility", place: "Electric Vehicles Dept · Bengaluru" },
    { year: "2018–2022", role: "Simulation engineer", org: "GTU Motorsports", place: "Formula Bharat · Gujarat" }
  ],

  patents: [
    { number: "IN 202441065103", title: "Thermal management of chargers", status: "Filed" },
    { number: "IN 202441065106", title: "Thermal management of energy storage devices", status: "Filed" }
  ],
  patentNote: "Covers India's first automated multi-pack thermal management system for a swapping station.",
  awards: [
    { year: "2025", name: "InvenZone Award", note: "Contribution to intellectual property" },
    { year: "2025", name: "Best Team Award", note: "Air-cool station & POC team" }
  ],

  // Photographs, not figures — so no FIG. number. The certificate is cropped
  // above its signatory block: the signature, seal and signing colleague's name
  // are out of frame rather than painted over.
  awardMedia: [
    {
      src: "assets/media/award-certificate.jpg",
      tag: "Best Team Award",
      caption: "Air-cool station & POC team, Q3 FY2025–26",
      alt: "SUN Mobility certificate of recognition, Best Team Award, awarded to Prince Chauhan"
    },
    {
      src: "assets/media/award-trophy.jpg",
      tag: "InvenZone Award",
      caption: "Awarded for intellectual-property contribution",
      alt: "InvenZone Awards 2025 trophy awarded to Prince Chauhan"
    }
  ],

  // His own words, from the high-ambient work. Kept because a stated engineering
  // position is the one thing a generic portfolio cannot fake.
  position: "A design that doesn't violate thermodynamics will hold at higher ambient. The answer is usually clarity, not complexity.",

  skills: [
    { domain: "Thermal design", tokens: ["BTMS", "CTMS", "heat-load estimation", "coolant-loop sizing", "radiator/chiller selection", "thermal-runaway prevention"] },
    { domain: "Simulation", tokens: ["ANSYS Fluent", "SolidWorks", "PTC Creo", "FEA"] },
    { domain: "Test & validation", tokens: ["chamber testing (−10 to 60 °C)", "IR thermography", "DAQ", "DOE", "RCA"] },
    { domain: "Systems & embedded", tokens: ["ECU simulation", "BMS architecture", "state-machine design", "CAN protocol"] }
  ],

  education: [
    { year: "2022", qual: "B.E., Automobile Engineering", inst: "LJIET, Gujarat", focus: "Heat transfer · Thermodynamics · Fluid mechanics" },
    { year: "2024", qual: "Astronautics & Human Spaceflight", inst: "MITx", focus: "" }
  ],

  contact: {
    availability: "Open to thermal roles in aerospace and spacecraft.",
    updated: "2026-09"
  },

  // The portrait enters as the drawing set's TITLE BLOCK — the cell that records
  // who drew the sheets — rather than as a seventh figure. That is why it carries
  // an attribution tag and no FIG. number. If the file is absent the whole block
  // is skipped at runtime, so the page never shows a hole or a broken image.
  portrait: {
    src: "assets/media/portrait.jpg",
    tag: "Drawn by",
    name: "Prince Chauhan",
    caption: "As built — to scale.",
    alt: "Portrait of Prince Chauhan, thermal engineer"
  }
};
