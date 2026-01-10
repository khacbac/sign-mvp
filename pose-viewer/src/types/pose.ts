export interface PoseKeypoint {
  name: string;
  coordinates: number[];
  confidence: number;
}

export interface PosePerson {
  person_id: number;
  keypoints: PoseKeypoint[];
}

export interface PoseFrame {
  frame: number;
  time: number;
  people: PosePerson[];
}

export interface PoseComponent {
  name: string;
  points: string[];
}

export interface PoseDimensions {
  width: number;
  height: number;
}

export interface PoseData {
  fps: number;
  dimensions: PoseDimensions;
  components: PoseComponent[];
  frames: PoseFrame[];
}
