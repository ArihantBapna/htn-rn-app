import {
  Center,
  NativeBaseProvider,
  VStack,
  Heading,
  Input,
  HStack,
  Button,
  useToast,
} from "native-base";
import NativeBaseIcon from "../../components/NativeBaseIcon";
import React, { useState } from "react";
import { useNavigation } from "@react-navigation/native";
import { createUserWithEmailAndPassword } from "firebase/auth";
import { auth } from "../../firebase";

export function RegisterPage() {
  const navigation = useNavigation();
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const toast = useToast();

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
            <Button onPress={RegisterUser}>Register</Button>
            <Button onPress={() => (navigation as any).navigate("home")}>
              Go to Login
            </Button>
          </HStack>
        </VStack>
      </Center>
    </NativeBaseProvider>
  );
}
