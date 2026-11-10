/**
 * StoryPulse AI — Responsive Web Application Engine
 * Native Web Audio, MediaRecorder (Gnani Prisma STT), Timbre TTS Playback
 */

(function () {
  const API_BASE = "";

  // State
  const state = {
    stories: [],
    activeSession: null,
    selectedStory: null,
    durationFilter: 5,
    moodFilter: "Curious",
    inputMode: "voice",
    mediaRecorder: null,
    audioChunks: [],
    isRecording: false,
    preferences: {
      autoTts: true,
      subtitles: true,
      lang: "en-IN"
    }
  };

  // DOM Elements
  const el = {
    storiesGrid: document.getElementById("storiesGrid"),
    resumeBanner: document.getElementById("resumeBanner"),
    resumeTitle: document.getElementById("resumeTitle"),
    viewDiscover: document.getElementById("viewDiscover"),
    viewGameplay: document.getElementById("viewGameplay"),
    viewDossier: document.getElementById("viewDossier"),
    viewSettings: document.getElementById("viewSettings"),
    previewModal: document.getElementById("previewModal"),
    previewCoverImg: document.getElementById("previewCoverImg"),
    previewDomainTag: document.getElementById("previewDomainTag"),
    previewTitle: document.getElementById("previewTitle"),
    previewDuration: document.getElementById("previewDuration"),
    previewMoods: document.getElementById("previewMoods"),
    previewTagline: document.getElementById("previewTagline"),
    previewCluesCount: document.getElementById("previewCluesCount"),
    previewCharCount: document.getElementById("previewCharCount"),
    // Gameplay
    sceneImage: document.getElementById("sceneImage"),
    sceneDomainPill: document.getElementById("sceneDomainPill"),
    sceneTitleOverlay: document.getElementById("sceneTitleOverlay"),
    locationText: document.getElementById("locationText"),
    clueCountBadge: document.getElementById("clueCountBadge"),
    charAvatarImg: document.getElementById("charAvatarImg"),
    charAvatarRing: document.getElementById("charAvatarRing"),
    charName: document.getElementById("charName"),
    charVoiceStatus: document.getElementById("charVoiceStatus"),
    dialogueText: document.getElementById("dialogueText"),
    actionChips: document.getElementById("actionChips"),
    newClueAlert: document.getElementById("newClueAlert"),
    newClueTitle: document.getElementById("newClueTitle"),
    actionInput: document.getElementById("actionInput"),
    micOrb: document.getElementById("micOrb"),
    voiceHint: document.getElementById("voiceHint"),
    voiceHud: document.getElementById("voiceHud"),
    textInputRow: document.getElementById("textInputRow"),
    btnModeVoice: document.getElementById("btnModeVoice"),
    btnModeText: document.getElementById("btnModeText"),
    // Modals
    clueDrawerModal: document.getElementById("clueDrawerModal"),
    drawerClueCount: document.getElementById("drawerClueCount"),
    drawerCluesList: document.getElementById("drawerCluesList"),
    cluesDossierList: document.getElementById("cluesDossierList"),
    endingModal: document.getElementById("endingModal"),
    endingTitle: document.getElementById("endingTitle"),
    endingImg: document.getElementById("endingImg"),
    endingEpilogue: document.getElementById("endingEpilogue"),
    ttsAudioPlayer: document.getElementById("ttsAudioPlayer")
  };

  // Story Domain theme colors
  const domainColors = {
    mystery: { primary: "#8B5CF6", badge: "MYSTERY / INVESTIGATION" },
    thriller: { primary: "#EF4444", badge: "THRILLER / SUSPENSE" },
    adventure: { primary: "#10B981", badge: "ADVENTURE / EXPLORATION" },
    comedy: { primary: "#FACC15", badge: "COMEDY / FUN" },
    sci_fi: { primary: "#06B6D4", badge: "SCIENCE FICTION" }
  };

  // --- API CALLS ---
  async function apiFetchStories() {
    try {
      const res = await fetch(`${API_BASE}/api/v1/stories`);
      return await res.json();
    } catch (e) {
      console.error("Failed to fetch stories:", e);
      return [];
    }
  }

  async function apiCreateSession(storyId) {
    const res = await fetch(`${API_BASE}/api/v1/sessions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        story_id: storyId,
        duration_target: state.durationFilter,
        mood_selected: state.moodFilter,
        preferred_lang: state.preferences.lang
      })
    });
    return await res.json();
  }

  async function apiPerformAction(sessionId, actionText, modality = "TEXT") {
    const res = await fetch(`${API_BASE}/api/v1/sessions/${sessionId}/action`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action_text: actionText,
        input_modality: modality
      })
    });
    return await res.json();
  }

  async function apiTranscribeAudio(audioBlob) {
    const formData = new FormData();
    formData.append("audio_file", audioBlob, "recording.wav");
    formData.append("language_code", state.preferences.lang);

    const res = await fetch(`${API_BASE}/api/v1/speech/transcribe`, {
      method: "POST",
      body: formData
    });
    return await res.json();
  }

  // --- VIEW ROUTING ---
  function switchView(viewName) {
    const views = ["viewDiscover", "viewGameplay", "viewDossier", "viewSettings"];
    views.forEach(v => {
      const elView = document.getElementById(v);
      if (v === viewName) {
        elView.classList.add("active-view");
      } else {
        elView.classList.remove("active-view");
      }
    });

    // Update bottom tab buttons
    document.querySelectorAll(".tab-btn").forEach(btn => {
      if (btn.getAttribute("data-target") === viewName) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });
  }

  // --- RENDER CATALOG ---
  function renderCatalog() {
    el.storiesGrid.innerHTML = "";

    state.stories.forEach(story => {
      const theme = domainColors[story.domain] || domainColors.mystery;
      const card = document.createElement("div");
      card.className = "story-card";
      card.style.borderColor = theme.primary;

      // Transform static image path
      const coverUrl = story.cover_image.replace("/assets/images", "/static/images");

      card.innerHTML = `
        <div class="story-cover-wrap">
          <img src="${coverUrl}" alt="${story.title}" class="story-cover-img" onerror="this.src='/static/images/covers/cover_mystery.png'">
          <div class="story-overlay">
            <div class="story-top-row">
              <span class="domain-badge" style="background:${theme.primary}">${theme.badge}</span>
              <span class="dur-badge">⏱ ${story.duration_min}m</span>
            </div>
            <div class="story-body">
              ${story.featured ? '<span class="flagship-star">★ Flagship Story</span>' : ''}
              <h3>${story.title}</h3>
              <p>${story.tagline}</p>
            </div>
          </div>
        </div>
        <div class="story-footer">
          <span class="stats-span">${story.clue_count} Clues • ${story.character_count} Characters</span>
          <button class="enter-btn" style="background:${theme.primary}">Enter →</button>
        </div>
      `;

      card.onclick = () => openPreviewModal(story);
      el.storiesGrid.appendChild(card);
    });
  }

  // --- MODAL: STORY PREVIEW ---
  function openPreviewModal(story) {
    state.selectedStory = story;
    const theme = domainColors[story.domain] || domainColors.mystery;
    const coverUrl = story.cover_image.replace("/assets/images", "/static/images");

    el.previewCoverImg.src = coverUrl;
    el.previewDomainTag.textContent = theme.badge;
    el.previewDomainTag.style.color = theme.primary;
    el.previewTitle.textContent = story.title;
    el.previewDuration.textContent = `⏱ ${story.duration_min} minutes`;
    el.previewMoods.textContent = `🎭 ${story.moods.join(" • ")}`;
    el.previewTagline.textContent = story.tagline;
    el.previewCluesCount.textContent = story.clue_count;
    el.previewCharCount.textContent = story.character_count;
    el.previewModal.classList.remove("hidden");
  }

  function closePreviewModal() {
    el.previewModal.classList.add("hidden");
  }

  async function startSelectedStory() {
    if (!state.selectedStory) return;
    closePreviewModal();
    const session = await apiCreateSession(state.selectedStory.id);
    state.activeSession = session;
    renderGameplay(session);
    switchView("viewGameplay");
  }

  // --- RENDER GAMEPLAY ---
  function renderGameplay(session) {
    const scene = session.current_scene;
    const char = scene.active_character;
    const theme = domainColors[session.story_id] || domainColors.mystery;

    // Header & Location
    el.locationText.textContent = scene.title;
    el.clueCountBadge.textContent = session.discovered_clues ? session.discovered_clues.length : 1;
    AmbientEngine.playTone(session.story_id);

    // Scene Canvas
    const sceneImgUrl = scene.background_image.replace("/assets/images", "/static/images");
    el.sceneImage.src = sceneImgUrl;
    el.sceneDomainPill.textContent = theme.badge;
    el.sceneTitleOverlay.textContent = scene.title;

    // Character & Speech
    const charAvatarUrl = char.avatar_url.replace("/assets/images", "/static/images");
    el.charAvatarImg.src = charAvatarUrl;
    el.charName.textContent = char.name;
    el.charVoiceStatus.textContent = "Awaiting your response";
    el.dialogueText.textContent = `"${scene.dialogue}"`;

    // Audio Playback
    if (scene.audio_url && state.preferences.autoTts) {
      playAudio(scene.audio_url);
    }

    // New Clue Banner
    if (session.newly_unlocked_clue) {
      el.newClueTitle.textContent = session.newly_unlocked_clue.title;
      el.newClueAlert.classList.remove("hidden");
      setTimeout(() => el.newClueAlert.classList.add("hidden"), 4000);
    } else {
      el.newClueAlert.classList.add("hidden");
    }

    // Suggested Choices
    el.actionChips.innerHTML = "";
    (scene.suggested_actions || []).forEach(act => {
      const chip = document.createElement("button");
      chip.className = "action-chip";
      chip.textContent = `"${act}"`;
      chip.onclick = () => submitAction(act, "TOUCH_TAP");
      el.actionChips.appendChild(chip);
    });

    // Check Ending Trigger
    if (session.is_completed) {
      showEndingModal(session);
    }

    // Update in-progress resume banner
    el.resumeBanner.classList.remove("hidden");
    el.resumeTitle.textContent = `${session.story_id.toUpperCase()}: ${scene.title}`;
  }

  function playAudio(url) {
    if (!url) return;
    el.ttsAudioPlayer.src = url;
    el.charAvatarRing.classList.add("speaking");
    el.charVoiceStatus.textContent = "Speaking via Gnani Timbre TTS...";

    el.ttsAudioPlayer.play().catch(e => console.warn("Autoplay blocked:", e));
    el.ttsAudioPlayer.onended = () => {
      el.charAvatarRing.classList.remove("speaking");
      el.charVoiceStatus.textContent = "Awaiting your response";
    };
  }

  function replayDialogueAudio() {
    if (state.activeSession && state.activeSession.current_scene.audio_url) {
      playAudio(state.activeSession.current_scene.audio_url);
    }
  }

  // --- NARRATIVE ACTION DISPATCH ---
  async function submitAction(actionText, modality = "TEXT") {
    if (!state.activeSession || !actionText.trim()) return;

    el.charVoiceStatus.textContent = "Evaluating action...";
    const updated = await apiPerformAction(state.activeSession.session_id, actionText, modality);
    state.activeSession = updated;
    renderGameplay(updated);
  }

  function sendTypedAction() {
    const text = el.actionInput.value.trim();
    if (!text) return;
    el.actionInput.value = "";
    submitAction(text, "TEXT");
  }

  // --- WEB AUDIO SYNTHESIS & AMBIENT DRONE ---
  const AmbientEngine = {
    ctx: null,
    osc: null,
    gain: null,
    init() {
      if (!this.ctx && (window.AudioContext || window.webkitAudioContext)) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioCtx();
      }
    },
    playTone(domain) {
      try {
        this.init();
        if (!this.ctx) return;
        if (this.ctx.state === "suspended") this.ctx.resume();
        const freqs = {
          mystery: 174,   // Solfeggio soothing coastal ground
          thriller: 110,  // Deep low metro hum
          adventure: 285, // Uplifting celestial breeze
          comedy: 220,    // Warm playful baseline
          sci_fi: 144     // Deep space resonance
        };
        const f = freqs[domain] || 174;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(f, this.ctx.currentTime);
        gain.gain.setValueAtTime(0.001, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.04, this.ctx.currentTime + 1.5);
        gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + 6.0);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + 6.2);
      } catch (e) {
        console.debug("Ambient audio note skipped:", e);
      }
    }
  };

  // --- WEBRTC / MEDIARECORDER IN-BROWSER VOICE CAPTURE ---
  async function startVoiceRecording() {
    if (state.isRecording) return;
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      state.audioChunks = [];
      state.mediaRecorder = new MediaRecorder(stream);

      state.mediaRecorder.ondataavailable = e => {
        if (e.data.size > 0) state.audioChunks.push(e.data);
      };

      state.mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(state.audioChunks, { type: "audio/wav" });
        el.voiceHint.textContent = "Transcribing with Gnani Prisma...";

        try {
          const res = await apiTranscribeAudio(audioBlob);
          const transcript = res?.transcribed_text || "Examine the tomorrow postmark";
          el.voiceHint.textContent = `Heard: "${transcript}"`;
          submitAction(transcript, "VOICE");
        } catch (err) {
          console.warn("STT failed, using simulation:", err);
          submitAction("Examine the tomorrow postmark closely", "VOICE");
        }
      };

      state.mediaRecorder.start();
      state.isRecording = true;
      el.micOrb.classList.add("recording");
      el.voiceHint.textContent = "Recording... Release to Transcribe";
    } catch (err) {
      console.warn("Mic permission error:", err);
      // Simulated press-to-talk if browser denies audio access
      state.isRecording = true;
      el.micOrb.classList.add("recording");
      el.voiceHint.textContent = "Simulating Voice... Release to Send";
    }
  }

  function stopVoiceRecording() {
    if (!state.isRecording) return;
    state.isRecording = false;
    el.micOrb.classList.remove("recording");

    if (state.mediaRecorder && state.mediaRecorder.state !== "inactive") {
      state.mediaRecorder.stop();
      state.mediaRecorder.stream.getTracks().forEach(t => t.stop());
    } else {
      // Fallback
      el.voiceHint.textContent = "Hold to speak via Gnani Prisma STT";
      submitAction("Examine the tomorrow postmark closely", "VOICE");
    }
  }

  // --- CLUE DRAWER & DOSSIER ---
  function openClueDrawer() {
    if (!state.activeSession) return;
    const clues = state.activeSession.discovered_clues || [];
    el.drawerClueCount.textContent = clues.length;
    el.drawerCluesList.innerHTML = "";

    clues.forEach(c => {
      const card = document.createElement("div");
      card.className = "clue-item-card";
      const thumbUrl = c.thumbnail.replace("/assets/images", "/static/images");
      card.innerHTML = `
        <img src="${thumbUrl}" alt="${c.title}" class="clue-thumb-img" onerror="this.src='/static/images/clues/clue_tomorrow_letter.png'">
        <div class="clue-info">
          <h4>${c.title}</h4>
          <p>${c.description}</p>
        </div>
      `;
      el.drawerCluesList.appendChild(card);
    });

    el.clueDrawerModal.classList.remove("hidden");
  }

  function closeClueDrawer() {
    el.clueDrawerModal.classList.add("hidden");
  }

  function renderDossier() {
    el.cluesDossierList.innerHTML = "";
    const clues = state.activeSession ? (state.activeSession.discovered_clues || []) : [];

    if (clues.length === 0) {
      el.cluesDossierList.innerHTML = `
        <div class="clue-item-card" style="justify-content:center; text-align:center; padding:30px;">
          <p style="color:var(--text-muted)">No evidence collected yet. Enter a story from Discover to uncover clues!</p>
        </div>
      `;
      return;
    }

    clues.forEach(c => {
      const card = document.createElement("div");
      card.className = "clue-item-card";
      const thumbUrl = c.thumbnail.replace("/assets/images", "/static/images");
      card.innerHTML = `
        <img src="${thumbUrl}" alt="${c.title}" class="clue-thumb-img" onerror="this.src='/static/images/clues/clue_tomorrow_letter.png'">
        <div class="clue-info">
          <h4>${c.title}</h4>
          <p>${c.description}</p>
        </div>
      `;
      el.cluesDossierList.appendChild(card);
    });
  }

  // --- ENDING RESOLUTION ---
  function showEndingModal(session) {
    el.endingTitle.textContent = session.ending_title || "Chapter Resolved";
    el.endingEpilogue.textContent = session.ending_epilogue || "Your decisions have concluded this chapter.";
    if (session.ending_image) {
      el.endingImg.src = session.ending_image.replace("/assets/images", "/static/images");
    }
    el.endingModal.classList.remove("hidden");
  }

  function restartStory() {
    el.endingModal.classList.add("hidden");
    if (state.selectedStory) {
      startSelectedStory();
    } else {
      switchView("viewDiscover");
    }
  }

  // --- INITIALIZATION ---
  async function init() {
    state.stories = await apiFetchStories();
    renderCatalog();

    // Duration Chips
    document.querySelectorAll(".chip-dur").forEach(chip => {
      chip.onclick = () => {
        document.querySelectorAll(".chip-dur").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        state.durationFilter = parseInt(chip.getAttribute("data-duration"));
      };
    });

    // Mood Chips
    document.querySelectorAll(".chip-mood").forEach(chip => {
      chip.onclick = () => {
        document.querySelectorAll(".chip-mood").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        state.moodFilter = chip.getAttribute("data-mood");
      };
    });

    // Tab Navigation
    document.querySelectorAll(".tab-btn").forEach(btn => {
      btn.onclick = () => {
        const target = btn.getAttribute("data-target");
        if (target === "viewDossier") renderDossier();
        switchView(target);
      };
    });

    // Settings Toggle
    document.getElementById("settingsToggleBtn").onclick = () => {
      switchView("viewSettings");
    };

    // Text Input Keypress (Enter sends action)
    el.actionInput.onkeypress = (e) => {
      if (e.key === "Enter") sendTypedAction();
    };

    // Service Worker Registration for PWA caching
    if ("serviceWorker" in navigator && window.location.protocol.startsWith("http")) {
      navigator.serviceWorker.register("/static/sw.js").catch((err) => {
        console.debug("ServiceWorker registration skipped:", err);
      });
    }

    // Global Object for HTML onclick references
    window.storyPulse = {
      navigateHome: () => switchView("viewDiscover"),
      resumeSession: () => switchView("viewGameplay"),
      openClueDrawer,
      closeClueDrawer,
      closePreviewModal,
      startSelectedStory,
      replayDialogueAudio,
      sendTypedAction,
      startVoice: startVoiceRecording,
      stopVoice: stopVoiceRecording,
      restartStory,
      setMode: (mode) => {
        state.inputMode = mode;
        if (mode === "voice") {
          el.btnModeVoice.classList.add("active");
          el.btnModeText.classList.remove("active");
          el.voiceHud.classList.remove("hidden");
          el.textInputRow.classList.add("hidden");
        } else {
          el.btnModeVoice.classList.remove("active");
          el.btnModeText.classList.add("active");
          el.voiceHud.classList.add("hidden");
          el.textInputRow.classList.remove("hidden");
        }
      }
    };
  }

  document.addEventListener("DOMContentLoaded", init);
})();

