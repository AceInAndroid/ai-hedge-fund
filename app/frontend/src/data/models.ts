import { api } from '@/services/api';

export interface LanguageModel {
  display_name: string;
  model_name: string;
  provider:
    | "Anthropic"
    | "Anthropic Compatible"
    | "DeepSeek"
    | "Google"
    | "GigaChat"
    | "Groq"
    | "LM Studio"
    | "OpenAI"
    | "OpenAI Compatible"
    | "OpenRouter"
    | "Azure OpenAI"
    | "xAI";
}

export const CUSTOM_MODEL_SENTINELS = new Set([
  "__custom_openai_compatible__",
  "__custom_anthropic_compatible__",
  "__lm_studio__",
]);

export const requiresCustomModelName = (model: LanguageModel | null): boolean =>
  !!model && CUSTOM_MODEL_SENTINELS.has(model.model_name);

// Cache for models to avoid repeated API calls
let languageModels: LanguageModel[] | null = null;

/**
 * Get the list of models from the backend API
 * Uses caching to avoid repeated API calls
 */
export const getModels = async (): Promise<LanguageModel[]> => {
  if (languageModels) {
    return languageModels;
  }
  
  try {
    languageModels = await api.getLanguageModels();
    return languageModels;
  } catch (error) {
    console.error('Failed to fetch models:', error);
    throw error; // Let the calling component handle the error
  }
};

/**
 * Get the default model (GPT-4.1) from the models list
 */
export const getDefaultModel = async (): Promise<LanguageModel | null> => {
  try {
    const models = await getModels();
    return models.find(model => model.model_name === "gpt-4.1") || models[0] || null;
  } catch (error) {
    console.error('Failed to get default model:', error);
    return null;
  }
};
