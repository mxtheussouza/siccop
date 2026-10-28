import { Tabs } from "expo-router";
import messages from "../../src/i18n/pt-BR.json";

export default function TabsLayout() {
  return (
    <Tabs screenOptions={{ headerShown: false }}>
      <Tabs.Screen name="index" options={{ title: messages.tabs.map }} />
      <Tabs.Screen name="incidents" options={{ title: messages.tabs.incidents }} />
      <Tabs.Screen name="operation" options={{ title: messages.tabs.operation }} />
      <Tabs.Screen name="alerts" options={{ title: messages.tabs.alerts }} />
      <Tabs.Screen name="profile" options={{ title: messages.tabs.profile }} />
    </Tabs>
  );
}
