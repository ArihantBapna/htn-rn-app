import {
  Button,
  Center,
  Heading,
  HStack, Image,
  Input,
  NativeBaseProvider,
  Switch,
  Text,
  useColorMode,
  useToast,
  VStack,
} from "native-base";
import NativeBaseIcon from "../../components/NativeBaseIcon";
import {
  createUserWithEmailAndPassword,
  onAuthStateChanged,
  signInWithEmailAndPassword,
} from "firebase/auth";
import React, { useState } from "react";
import { auth } from "../../firebase";
import { useNavigation } from "@react-navigation/native";
import {ImageBackground, View} from "react-native";

// @ts-ignore
import image from "./assets/bg.png"
// @ts-ignore
import logo from "./assets/squirrel_logo.png"

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

  // Sign up a user
  function RegisterUser() {
    createUserWithEmailAndPassword(auth, email, password)
      .then((userCred) => {
        const user = userCred.user;
        console.log("User created:" + user);
        (navigation as any).navigate("home");
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
      <ImageBackground resizeMode='cover'  source={image} style={{width: "100%", height: "100%"}}>
        <View style={{
          flex: 1,
          justifyContent: "center",
          alignItems: "center"
        }}>
          <Center
              px={4}
              flex={1}
          >
            <VStack space={5} alignItems="center">
              <Image source={logo} alt="Squirrel Logo" size="xl" />
              <Heading size="lg">Welcome to SquirrelAI</Heading>
              <VStack space={2} width={"auto"} alignItems="center">
                <Input
                    type={"text"}
                    value={email}
                    backgroundColor={"rgba(224,178,147,0.09)"}
                    onChangeText={setEmail}
                    width={"100%"}
                    height={"40px"}
                    variant="underlined"
                    px={4}
                    placeholder="Email"
                />
                <Input
                    type={"password"}
                    value={password}
                    backgroundColor={"rgba(224,178,147,0.09)"}
                    onChangeText={setPassword}
                    width={"100%"}
                    height={"40px"}
                    variant="underlined"
                    px={4}
                    placeholder="Password"
                />
              </VStack>
              <HStack space={2}>
                <Button onPress={LoginUser} backgroundColor={"#C98860"}>Login</Button>
                <Button onPress={RegisterUser} backgroundColor={"#C98860"}>Register</Button>
              </HStack>
            </VStack>
          </Center>
        </View>
      </ImageBackground>
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
