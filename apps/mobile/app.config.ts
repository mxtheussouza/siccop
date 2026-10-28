import type { ExpoConfig } from "expo/config";
import messages from "./src/i18n/pt-BR.json";

const config: ExpoConfig = {
  name: messages.app.name,
  slug: "operational-platform",
  scheme: "operational-platform",
  version: "0.1.0",
  orientation: "default",
  userInterfaceStyle: "automatic",
  plugins: ["expo-router", "expo-dev-client"],
  ios: { supportsTablet: true, bundleIdentifier: "org.operationalplatform.mobile" },
  android: { package: "org.operationalplatform.mobile" },
  experiments: { typedRoutes: true },
};

export default config;
