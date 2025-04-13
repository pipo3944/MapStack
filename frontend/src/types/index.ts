// ユーザー関連の型
export interface User {
  id: string;
  name: string;
  email: string;
  profileImage?: string;
  createdAt: string;
  updatedAt: string;
}

// ロードマップ関連の型
export interface Roadmap {
  id: string;
  title: string;
  description: string;
  category: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimatedHours: number;
  topics: RoadmapTopic[];
  createdAt: string;
  updatedAt: string;
}

export interface RoadmapTopic {
  id: string;
  title: string;
  description: string;
  order: number;
  resources: Resource[];
  exercises: Exercise[];
}

// リソース関連の型
export interface Resource {
  id: string;
  title: string;
  description: string;
  type: 'article' | 'video' | 'book' | 'course';
  url: string;
  durationMinutes: number;
}

// 演習関連の型
export interface Exercise {
  id: string;
  title: string;
  description: string;
  difficulty: 'easy' | 'medium' | 'hard';
  type: 'quiz' | 'project' | 'challenge';
  estimatedMinutes: number;
}

// プログレス関連の型
export interface UserProgress {
  userId: string;
  roadmapId: string;
  topicId: string;
  completedResources: string[]; // resourceIds
  completedExercises: string[]; // exerciseIds
  startedAt: string;
  lastAccessedAt: string;
  completedAt?: string;
}
