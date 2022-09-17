import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { NativeWindStyleSheet } from "nativewind";
import HomePage from "./pages/Home";


const Stack = createNativeStackNavigator();

NativeWindStyleSheet.setOutput({
    default: "native",
});

export default function App() {
  return (
      <NavigationContainer>
        <Stack.Navigator>
          <Stack.Screen name="home" component={HomePage} options={{headerShown: false}} />
        </Stack.Navigator>
      </NavigationContainer>
  );
}


