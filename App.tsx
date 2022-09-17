import React from "react";
import {
  extendTheme,
    NativeBaseProvider,
} from "native-base";
import {createNativeStackNavigator} from "@react-navigation/native-stack";
import {NavigationContainer} from "@react-navigation/native";
import LoginPage from "./pages/Login";
import RegisterPage from "./pages/Register";

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
  return (
      <NativeBaseProvider>
          <NavigationContainer>
              <Stack.Navigator>
                  <Stack.Screen name={"login"} component={LoginPage} options={{headerShown: false}} />
                  <Stack.Screen name={"register"} component={RegisterPage} options={{headerShown: false}} />
              </Stack.Navigator>
          </NavigationContainer>
      </NativeBaseProvider>
  );
}


