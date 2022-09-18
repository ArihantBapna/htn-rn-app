import { signOut } from "@firebase/auth";
import {
  Button,
  Box,
  useToast,
  Center,
  ScrollView,
  Heading,
  HStack,
  Image,
  IconButton,
} from "native-base";
import { auth, db } from "../../firebase";
import { Audio } from "expo-av";
import { useEffect, useState } from "react";
import { Recording } from "expo-av/build/Audio/Recording";
import { getStorage, ref, uploadBytes, getDownloadURL } from "firebase/storage";
import { doc, setDoc } from "firebase/firestore";
import { collection, query, where, onSnapshot } from "firebase/firestore";
import {ImageBackground, Linking, TouchableOpacity, View} from "react-native";
import { useCollection } from "react-firebase-hooks/firestore";
import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";
// @ts-ignore
import image from "./assets/bg.png";
// @ts-ignore
import record from "./assets/main_button.png";
// @ts-ignore
import logout from "./assets/logout.png";

export function HomePage() {
  const toast = useToast();
  const [recording, setRecording] = useState<Recording>();
  const [recordings, setRecordings] = useState<any[]>([]);

  const navigation = useNavigation();

  async function startRecording() {
    try {
      await Audio.requestPermissionsAsync();
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });
      const { recording } = await Audio.Recording.createAsync(
        Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY
      );
      setRecording(recording);
    } catch (err) {
      console.error("Failed to start recording", err);
    }
  }

  function callTheApi(fileName: string, fileUrl: string, userId: string) {
    // Do shit with the file data
    console.log(fileName, fileUrl, userId);
  }

  async function stopRecording() {
    await recording?.stopAndUnloadAsync();
    const uri = recording?.getURI();
    setRecording(undefined);
    if (uri) {
      await fetch(uri).then((r) => {
        r.blob().then((blob) => {
          const storage = getStorage();
          const time = new Date().getMilliseconds().toString();
          const extension = `${blob.type.split("/")[1]}`;
          const storageRef = ref(
            storage,
            `${auth.currentUser?.uid}/${time}.${extension}`
          );
          uploadBytes(storageRef, blob)
            .then((snapshot) => {
              console.log("Uploaded this shit");
              toast.show({
                title: "Uploaded Audio file successfully",
                backgroundColor: "green.500",
              });
              getDownloadURL(snapshot.ref)
                .then(async (url) => {
                  console.log("Found the url");
                  await setDoc(
                    doc(db, `${auth.currentUser?.uid}`, `${time}.${extension}`),
                    {
                      flashcards: "[]",
                      url: url,
                      name: `${time}.${extension}`,
                      userid: auth.currentUser?.uid,
                    }
                  );
                  console.log("Done");
                })
                .catch((err) => {
                  toast.show({
                    title: "Error getting download url",
                    backgroundColor: "red.500",
                  });
                });
            })
            .catch((e) => {
              toast.show({
                title: "Error uploading audio file",
                backgroundColor: "red.500",
              });
            });
        });
      });
    }
  }

  const [value, loading, error] = useCollection(
    collection(db, `${auth.currentUser?.uid}`)
  );

  useEffect(() => {
    if (value && !loading) {
      let newDocs: any[] = [];
      value.docs.forEach((doc) => {
        newDocs.push(doc.data());
      });
      setRecordings(newDocs);
    }
  }, [value, loading]);

  return (
      <ImageBackground resizeMode='cover'  source={image} style={{width: "100%", height: "100%"}}>
          <View style={{
              flex: 1,
              justifyContent: "center",
              alignItems: "center"
          }}>
              <Box height={"100%"} px={8} safeArea>
                  <Center>
                      <Heading mt={8} textAlign={"center"}>Your Recordings</Heading>
                      <HStack justifyContent={"space-between"} alignItems={"center"}>
                          <Center>
                              {recording == null ? (
                                  <TouchableOpacity onPress={startRecording}>
                                      <Image source={record} alt="Squirrel Logo" width={"141px"} height={"56px"} />
                                  </TouchableOpacity>
                              ) : (
                                  <Button onPress={stopRecording} backgroundColor={"#C98860"}>
                                      Stop Recording
                                  </Button>
                              )}
                          </Center>
                      </HStack>
                      <ScrollView
                          w={"100%"}
                          maxHeight={"75%"}
                          style={{ display: "flex", flexGrow: 1, flexDirection: "column" }}
                      >
                          {recordings.map((recording, index) => {
                              return (
                                  <HStack
                                      key={index}
                                      justifyContent={"space-between"}
                                      alignItems={"center"}
                                      my={3}
                                  >
                                      <Heading>{recording.name}</Heading>
                                      <HStack space={2} alignItems={"center"} display={"flex"}>
                                          <IconButton
                                              icon={<Ionicons name="download" size={24} color="black" />}
                                              onPress={() => {
                                                  Linking.openURL(recording.url)
                                                      .then()
                                                      .catch((err) => {
                                                          toast.show({
                                                              title: "Error opening file",
                                                              backgroundColor: "red.500",
                                                          });
                                                      });
                                              }}
                                          />
                                          <IconButton
                                              onPress={() => {
                                                  (navigation as any).navigate("transcript", {
                                                      recording: recordings[index],
                                                  });
                                              }}
                                              icon={
                                                  <Ionicons
                                                      name={"clipboard-outline"}
                                                      size={24}
                                                      color={"black"}
                                                  />
                                              }
                                          />
                                          <IconButton
                                              onPress={() => {
                                                  (navigation as any).navigate("slides", {
                                                      recording: recordings[index],
                                                  });
                                              }}
                                              icon={
                                                  <Ionicons
                                                      name={"albums-outline"}
                                                      size={24}
                                                      color={"black"}
                                                  />
                                              }
                                          />
                                      </HStack>
                                  </HStack>
                              );
                          })}
                      </ScrollView>
                  </Center>
                  <TouchableOpacity onPress={() => {
                      signOut(auth)
                          .then()
                          .catch((error) => {
                              toast.show({
                                  title: error.code,
                                  description: error.message,
                                  backgroundColor: "red.600",
                              });
                          });
                  }}>
                        <Image source={logout} alt="Squirrel Logo" width={"100%"} height={"40px"} />
                  </TouchableOpacity>
              </Box>
          </View>
      </ImageBackground>

  );
}
