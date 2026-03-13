import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { apiKeysService } from '@/services/api-keys-api';
import { Eye, EyeOff, Key, Link2, Trash2 } from 'lucide-react';
import { type ReactNode, useEffect, useState } from 'react';

interface ApiSettingField {
  key: string;
  label: string;
  description: string;
  placeholder: string;
  kind: 'secret' | 'text';
  url?: string;
}

const FINANCIAL_API_FIELDS: ApiSettingField[] = [
  {
    key: 'FINANCIAL_DATASETS_API_KEY',
    label: 'Financial Datasets API Key',
    description: 'Financial market data used by the hedge fund agents.',
    placeholder: 'your-financial-datasets-api-key',
    kind: 'secret',
    url: 'https://financialdatasets.ai/',
  },
];

const MARKET_DATA_FIELDS: ApiSettingField[] = [
  {
    key: 'PRICE_DATA_SOURCES',
    label: 'Price Data Source Order',
    description:
      'Comma-separated fallback order for price queries. Supported values: financial_datasets, akshare, baostock, tushare, tencent, xueqiu, baidu.',
    placeholder: 'financial_datasets,akshare,baostock,tushare,tencent,xueqiu,baidu',
    kind: 'text',
  },
  {
    key: 'TUSHARE_TOKEN',
    label: 'Tushare Token',
    description: 'Optional. Required only when tushare is included in the fallback chain.',
    placeholder: 'your-tushare-token',
    kind: 'secret',
    url: 'https://tushare.pro/',
  },
];

const OFFICIAL_PROVIDER_FIELDS: ApiSettingField[] = [
  {
    key: 'OPENAI_API_KEY',
    label: 'OpenAI API Key',
    description: 'Used for official OpenAI models.',
    placeholder: 'your-openai-api-key',
    kind: 'secret',
    url: 'https://platform.openai.com/',
  },
  {
    key: 'OPENAI_API_BASE',
    label: 'OpenAI Base URL',
    description: 'Optional. Override the default OpenAI endpoint.',
    placeholder: 'https://api.openai.com/v1',
    kind: 'text',
  },
  {
    key: 'ANTHROPIC_API_KEY',
    label: 'Anthropic API Key',
    description: 'Used for official Claude models.',
    placeholder: 'your-anthropic-api-key',
    kind: 'secret',
    url: 'https://console.anthropic.com/',
  },
  {
    key: 'ANTHROPIC_BASE_URL',
    label: 'Anthropic Base URL',
    description: 'Optional. Override the default Anthropic endpoint.',
    placeholder: 'https://api.anthropic.com/v1',
    kind: 'text',
  },
];

const COMPATIBLE_PROVIDER_FIELDS: ApiSettingField[] = [
  {
    key: 'OPENAI_COMPATIBLE_API_KEY',
    label: 'OpenAI-Compatible API Key',
    description: 'Used when a node selects the custom OpenAI-compatible protocol.',
    placeholder: 'your-compatible-api-key',
    kind: 'secret',
  },
  {
    key: 'OPENAI_COMPATIBLE_BASE_URL',
    label: 'OpenAI-Compatible Base URL',
    description: 'Example: https://your-host/v1',
    placeholder: 'https://your-host/v1',
    kind: 'text',
  },
  {
    key: 'ANTHROPIC_COMPATIBLE_API_KEY',
    label: 'Anthropic-Compatible API Key',
    description: 'Used when a node selects the custom Anthropic-compatible protocol.',
    placeholder: 'your-compatible-api-key',
    kind: 'secret',
  },
  {
    key: 'ANTHROPIC_COMPATIBLE_BASE_URL',
    label: 'Anthropic-Compatible Base URL',
    description: 'Example: https://your-host/v1',
    placeholder: 'https://your-host/v1',
    kind: 'text',
  },
  {
    key: 'LM_STUDIO_API_KEY',
    label: 'LM Studio API Key',
    description: 'Optional. Leave empty if your LM Studio server does not require auth.',
    placeholder: 'lm-studio',
    kind: 'secret',
  },
  {
    key: 'LM_STUDIO_BASE_URL',
    label: 'LM Studio Base URL',
    description: 'Default local endpoint used by LM Studio.',
    placeholder: 'http://127.0.0.1:1234/v1',
    kind: 'text',
  },
];

export function ApiKeysSettings() {
  const [settings, setSettings] = useState<Record<string, string>>({});
  const [visibleSecrets, setVisibleSecrets] = useState<Record<string, boolean>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      setLoading(true);
      setError(null);
      const summaries = await apiKeysService.getAllApiKeys();

      const loadedSettings: Record<string, string> = {};
      for (const summary of summaries) {
        try {
          const fullValue = await apiKeysService.getApiKey(summary.provider);
          loadedSettings[summary.provider] = fullValue.key_value;
        } catch (err) {
          console.warn(`Failed to load setting for ${summary.provider}:`, err);
        }
      }

      setSettings(loadedSettings);
    } catch (err) {
      console.error('Failed to load API settings:', err);
      setError('Failed to load API settings. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleValueChange = async (key: string, value: string) => {
    setSettings((prev) => ({
      ...prev,
      [key]: value,
    }));

    try {
      if (value.trim()) {
        await apiKeysService.createOrUpdateApiKey({
          provider: key,
          key_value: value.trim(),
          is_active: true,
        });
      } else {
        try {
          await apiKeysService.deleteApiKey(key);
        } catch (err) {
          console.log(`Setting ${key} not found for deletion, which is expected`);
        }
      }
    } catch (err) {
      console.error(`Failed to save setting ${key}:`, err);
      setError(`Failed to save ${key}. Please try again.`);
    }
  };

  const toggleSecretVisibility = (key: string) => {
    setVisibleSecrets((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const clearSetting = async (key: string) => {
    try {
      await apiKeysService.deleteApiKey(key);
      setSettings((prev) => {
        const next = { ...prev };
        delete next[key];
        return next;
      });
    } catch (err) {
      console.error(`Failed to delete setting ${key}:`, err);
      setError(`Failed to delete ${key}. Please try again.`);
    }
  };

  const renderSection = (
    title: string,
    description: string,
    fields: ApiSettingField[],
    icon: ReactNode
  ) => (
    <Card className="bg-panel border-gray-700 dark:border-gray-700">
      <CardHeader>
        <CardTitle className="text-lg font-medium text-primary flex items-center gap-2">
          {icon}
          {title}
        </CardTitle>
        <p className="text-sm text-muted-foreground">{description}</p>
      </CardHeader>
      <CardContent className="space-y-4">
        {fields.map((field) => {
          const isSecret = field.kind === 'secret';
          const hasValue = !!settings[field.key];

          return (
            <div key={field.key} className="space-y-2">
              {field.url ? (
                <button
                  className="text-sm font-medium text-primary hover:text-blue-500 cursor-pointer transition-colors text-left"
                  onClick={() => window.open(field.url, '_blank')}
                >
                  {field.label}
                </button>
              ) : (
                <div className="text-sm font-medium text-primary">{field.label}</div>
              )}
              <p className="text-xs text-muted-foreground">{field.description}</p>
              <div className="relative">
                <Input
                  type={isSecret && !visibleSecrets[field.key] ? 'password' : 'text'}
                  placeholder={field.placeholder}
                  value={settings[field.key] || ''}
                  onChange={(e) => handleValueChange(field.key, e.target.value)}
                  className={hasValue || isSecret ? 'pr-20' : undefined}
                />
                {hasValue && (
                  <div className="absolute right-1 top-1/2 -translate-y-1/2 flex items-center gap-1">
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-7 w-7 hover:bg-red-500/10 hover:text-red-500"
                      onClick={() => clearSetting(field.key)}
                    >
                      <Trash2 className="h-3 w-3" />
                    </Button>
                    {isSecret && (
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-7 w-7"
                        onClick={() => toggleSecretVisibility(field.key)}
                      >
                        {visibleSecrets[field.key] ? (
                          <EyeOff className="h-3 w-3" />
                        ) : (
                          <Eye className="h-3 w-3" />
                        )}
                      </Button>
                    )}
                  </div>
                )}
                {!hasValue && isSecret && (
                  <div className="absolute right-1 top-1/2 -translate-y-1/2">
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-7 w-7"
                      onClick={() => toggleSecretVisibility(field.key)}
                    >
                      {visibleSecrets[field.key] ? (
                        <EyeOff className="h-3 w-3" />
                      ) : (
                        <Eye className="h-3 w-3" />
                      )}
                    </Button>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-xl font-semibold text-primary mb-2">API Settings</h2>
          <p className="text-sm text-muted-foreground">Loading API settings...</p>
        </div>
        <Card className="bg-panel border-gray-700 dark:border-gray-700">
          <CardContent className="p-6">
            <div className="text-sm text-muted-foreground">
              Please wait while we load your API settings...
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-primary mb-2">API Settings</h2>
        <p className="text-sm text-muted-foreground">
          Configure credentials and endpoint URLs for financial data, official model providers,
          and protocol-compatible backends.
        </p>
      </div>

      {error && (
        <Card className="bg-red-500/5 border-red-500/20">
          <CardContent className="p-4">
            <div className="flex items-start gap-3">
              <Key className="h-5 w-5 text-red-500 mt-0.5 flex-shrink-0" />
              <div className="space-y-1">
                <h4 className="text-sm font-medium text-red-500">Error</h4>
                <p className="text-xs text-muted-foreground">{error}</p>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setError(null);
                    loadSettings();
                  }}
                  className="text-xs mt-2 p-0 h-auto text-red-500 hover:text-red-400"
                >
                  Try again
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {renderSection(
        'Financial Data',
        'API credentials required for market and fundamentals data.',
        FINANCIAL_API_FIELDS,
        <Key className="h-4 w-4" />
      )}

      {renderSection(
        'Market Data Sources',
        'Configure the fallback order for A-share price data. Akshare, Baostock, Tencent, Xueqiu, and Baidu do not require keys here.',
        MARKET_DATA_FIELDS,
        <Link2 className="h-4 w-4" />
      )}

      {renderSection(
        'Official Providers',
        'Keys and optional endpoint overrides for direct OpenAI and Anthropic access.',
        OFFICIAL_PROVIDER_FIELDS,
        <Link2 className="h-4 w-4" />
      )}

      {renderSection(
        'Compatible Protocols',
        'Reusable endpoint settings for OpenAI-compatible services, Anthropic-compatible services, and LM Studio.',
        COMPATIBLE_PROVIDER_FIELDS,
        <Link2 className="h-4 w-4" />
      )}

      <Card className="bg-amber-500/5 border-amber-500/20">
        <CardContent className="p-4">
          <div className="flex items-start gap-3">
            <Key className="h-5 w-5 text-amber-500 mt-0.5 flex-shrink-0" />
            <div className="space-y-1">
              <h4 className="text-sm font-medium text-amber-500">Security Note</h4>
              <p className="text-xs text-muted-foreground">
                Settings are stored locally by this app. Keep secret keys private and prefer local
                endpoints for LM Studio or self-hosted gateways when possible.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
