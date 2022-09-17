import {
  Button,
  Center,
  Heading,
  HStack,
  Input,
  NativeBaseProvider,
  Switch,
  Text,
  useColorMode,
  useToast,
  VStack,
} from "native-base";
import NativeBaseIcon from "../../components/NativeBaseIcon";
import { onAuthStateChanged, signInWithEmailAndPassword } from "firebase/auth";
import React, { useState } from "react";
import { auth } from "../../firebase";
import { useNavigation } from "@react-navigation/native";

export function LoginPage() {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const toast = useToast();

  const navigation = useNavigation();

  // Function try Logging in to the service
  function LoginUser() {
    signInWithEmailAndPassword(auth, email, password)
      .then((userCred) => {
        const user = userCred.user;
      })
      .catch((error) => {
        toast.show({
          title: error.code,
          description: error.message,
          backgroundColor: "red.600",
        });
      });
  }

  return (
    <NativeBaseProvider>
      <Center
        _dark={{ bg: "blueGray.900" }}
        _light={{ bg: "blueGray.50" }}
        px={4}
        flex={1}
      >
        <VStack space={5} alignItems="center">
          <NativeBaseIcon />
          <Heading size="lg">Welcome to Squirrel</Heading>
          <VStack space={2} width={"auto"} alignItems="center">
            <Input
              type={"text"}
              value={email}
              onChangeText={setEmail}
              width={"100%"}
              height={"40px"}
              variant="outline"
              placeholder="Email"
            />
            <Input
              type={"password"}
              value={password}
              onChangeText={setPassword}
              width={"100%"}
              height={"40px"}
              variant="outline"
              placeholder="Password"
            />
          </VStack>
          <HStack space={2}>
            <Button onPress={LoginUser}>Login</Button>
            <Button onPress={() => (navigation as any).navigate("register")}>
              Go to Register
            </Button>
          </HStack>
          <ToggleDarkMode />
        </VStack>
      </Center>
    </NativeBaseProvider>
  );
}

// Color Switch Component
export function ToggleDarkMode() {
  const { colorMode, toggleColorMode } = useColorMode();
  return (
    <HStack space={2} alignItems="center">
      <Text>Dark</Text>
      <Switch
        isChecked={colorMode === "light"}
        onToggle={toggleColorMode}
        aria-label={
          colorMode === "light" ? "switch to dark mode" : "switch to light mode"
        }
      />
      <Text>Light</Text>
    </HStack>
  );
}
