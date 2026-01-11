import { useState } from "react";
import { PoseViewer } from "react-pose-viewer";
import "./App.css";

// Get URL parameter on initial load
const getInitialUrl = () => {
  const params = new URLSearchParams(window.location.search);
  return params.get("url") || "http://localhost:8000/output/poses/sample.pose";
};

function App() {
  const initialUrl = getInitialUrl();
  const [poseUrl, setPoseUrl] = useState(initialUrl);
  const [loadedUrl, setLoadedUrl] = useState(initialUrl);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [autoplay, setAutoplay] = useState(!!initialUrl);
  const [loop, setLoop] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadPoseData = () => {
    if (!poseUrl.trim()) {
      setError("Please enter a URL");
      return;
    }

    setError(null);
    setLoadedUrl(poseUrl);
    setAutoplay(true);
  };

  return (
    <div style={{ padding: "20px", maxWidth: "1200px", margin: "0 auto" }}>
      <h1>Pose Viewer</h1>

      <div style={{ marginBottom: "20px" }}>
        <div style={{ display: "flex", gap: "10px", marginBottom: "10px" }}>
          <input
            type="text"
            value={poseUrl}
            onChange={(e) => setPoseUrl(e.target.value)}
            placeholder="Enter pose file URL (.pose file)"
            style={{
              flex: 1,
              padding: "10px",
              fontSize: "14px",
              borderRadius: "4px",
              border: "1px solid #ccc",
            }}
            onKeyPress={(e) => e.key === "Enter" && loadPoseData()}
          />
          <button
            onClick={loadPoseData}
            style={{
              padding: "10px 20px",
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
              fontSize: "14px",
            }}
          >
            Load Pose
          </button>
        </div>

        {error && (
          <div
            style={{
              padding: "10px",
              backgroundColor: "#ffebee",
              color: "#c62828",
              borderRadius: "4px",
            }}
          >
            {error}
          </div>
        )}
      </div>

      {/* Controls */}
      <div
        style={{
          marginBottom: "20px",
          padding: "15px",
          backgroundColor: "#f5f5f5",
          borderRadius: "8px",
        }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "15px",
          }}
        >
          <div>
            <label style={{ display: "block", marginBottom: "5px" }}>
              <input
                type="checkbox"
                checked={autoplay}
                onChange={(e) => setAutoplay(e.target.checked)}
                style={{ marginRight: "5px" }}
              />
              Autoplay
            </label>
          </div>

          <div>
            <label style={{ display: "block", marginBottom: "5px" }}>
              <input
                type="checkbox"
                checked={loop}
                onChange={(e) => setLoop(e.target.checked)}
                style={{ marginRight: "5px" }}
              />
              Loop
            </label>
          </div>

          <div style={{ gridColumn: "1 / -1" }}>
            <label style={{ display: "block", marginBottom: "5px" }}>
              Playback Speed: {playbackSpeed}x
            </label>
            <input
              type="range"
              min="0.25"
              max="2"
              step="0.25"
              value={playbackSpeed}
              onChange={(e) => setPlaybackSpeed(parseFloat(e.target.value))}
              style={{ width: "100%" }}
            />
          </div>
        </div>
      </div>

      {loadedUrl ? (
        <div
          style={{
            border: "1px solid #ccc",
            borderRadius: "8px",
            overflow: "hidden",
            backgroundColor: "#000",
            width: "100%",
            minHeight: "600px",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <PoseViewer
            src={loadedUrl}
            loop={loop}
            autoplay={autoplay}
            playbackRate={playbackSpeed}
            height="600px"
            width="800px"
            background="#000000"
            thickness={2}
          />
        </div>
      ) : (
        <div
          style={{
            textAlign: "center",
            padding: "60px",
            color: "#666",
            backgroundColor: "#f5f5f5",
            borderRadius: "8px",
            border: "2px dashed #ccc",
          }}
        >
          <p style={{ fontSize: "18px", marginBottom: "10px" }}>
            Enter a pose file URL to get started
          </p>
          <p style={{ fontSize: "14px", color: "#999" }}>
            Example: http://localhost:8000/text-to-pose?text=hello
          </p>
          <p style={{ fontSize: "12px", color: "#999", marginTop: "10px" }}>
            Supports .pose file format
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
