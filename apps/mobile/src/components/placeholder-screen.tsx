import { StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import messages from "../i18n/pt-BR.json";

export function PlaceholderScreen({ title }: { title: string }) {
  return (
    <SafeAreaView style={styles.safe}>
      <View style={styles.content}>
        <Text accessibilityRole="header" style={styles.heading}>
          {title}
        </Text>
        <Text style={styles.status}>{messages.bootstrap.title}</Text>
        <Text style={styles.description}>{messages.bootstrap.description}</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#f4f6f8" },
  content: { padding: 24, width: "100%", maxWidth: 720, alignSelf: "center" },
  heading: {
    color: "#172535",
    fontSize: 28,
    fontWeight: "600",
    marginBottom: 24,
  },
  status: {
    color: "#173a50",
    fontSize: 20,
    fontWeight: "600",
    marginBottom: 12,
  },
  description: { color: "#334155", fontSize: 16, lineHeight: 26 },
});
