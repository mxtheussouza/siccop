import { render, screen } from "@testing-library/react-native";
import { PlaceholderScreen } from "../src/components/placeholder-screen";
import messages from "../src/i18n/pt-BR.json";

describe("bootstrap boundary", () => {
  it("announces that operational features are not implemented", () => {
    render(<PlaceholderScreen title={messages.tabs.map} />);
    expect(screen.getByRole("header", { name: messages.tabs.map })).toBeTruthy();
    expect(screen.getByText(messages.bootstrap.title)).toBeTruthy();
    expect(screen.queryByRole("button")).toBeNull();
  });
});
