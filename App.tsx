import React, { useState } from "react";
import { extendTheme, NativeBaseProvider } from "native-base";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { NavigationContainer } from "@react-navigation/native";
import LoginPage from "./pages/Login";
import HomePage from "./pages/Home";
import { auth } from "./firebase";
import { onAuthStateChanged } from "firebase/auth";
import TranscriptPage from "./pages/Transcript";

// Define the config
const config = {
  useSystemColorMode: false,
  initialColorMode: "dark",
};

// extend the theme
export const theme = extendTheme({ config });
type MyThemeType = typeof theme;
declare module "native-base" {
  interface ICustomTheme extends MyThemeType {}
}

const Stack = createNativeStackNavigator();

export default function App() {
  const [isSignedIn, setIsSignedIn] = useState<boolean>(
    auth.currentUser != null
  );

  onAuthStateChanged(auth, (user) => {
    setIsSignedIn(user != null);
  });

  return (
    <NativeBaseProvider>
      <NavigationContainer>
        <Stack.Navigator>
          {isSignedIn ? (
            <>
              <Stack.Screen
                name={"homePage"}
                component={HomePage}
                options={{ headerShown: false }}
              />
              <Stack.Screen
                name={"transcript"}
                component={TranscriptPage}
                options={{ headerShown: false }}
              />
            </>
          ) : (
            <>
              <Stack.Screen
                name={"home"}
                component={LoginPage}
                options={{ headerShown: false }}
              />
            </>
          )}
        </Stack.Navigator>
      </NavigationContainer>
    </NativeBaseProvider>
  );
}
