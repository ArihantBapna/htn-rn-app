import { signOut } from "@firebase/auth";
import {
  Button,
  Box,
  useToast,
  Center,
  ScrollView,
  Heading,
  Text,
  HStack,
} from "native-base";
import { auth, db } from "../../firebase";
import { Audio } from "expo-av";
import { useEffect, useState } from "react";
import { Recording } from "expo-av/build/Audio/Recording";
import { getStorage, ref, uploadBytes, getDownloadURL } from "firebase/storage";
import { doc, setDoc } from "firebase/firestore";
import { collection, query, where, onSnapshot } from "firebase/firestore";
import { Linking } from "react-native";
import { useCollection } from "react-firebase-hooks/firestore";

export function HomePage() {
  const toast = useToast();
  const [recording, setRecording] = useState<Recording>();
  const [recordings, setRecordings] = useState<any[]>([]);

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
    <Box height={"100%"} px={8} safeArea>
      <Heading textAlign={"center"}>Your Recordings</Heading>

      <Center my={4}>
        <HStack justifyContent={"space-between"} alignItems={"center"}>
          <Center>
            {recording == null ? (
              <Button onPress={startRecording} backgroundColor={"red.500"}>
                Start Recording
              </Button>
            ) : (
              <Button onPress={stopRecording} backgroundColor={"green.500"}>
                Stop Recording
              </Button>
            )}
          </Center>
        </HStack>
      </Center>

      <Center my={4}>
        <ScrollView
          w={"100%"}
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
                <Button
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
                >
                  Open
                </Button>
              </HStack>
            );
          })}
        </ScrollView>
      </Center>
      <Button
        onPress={() => {
          signOut(auth)
            .then()
            .catch((error) => {
              toast.show({
                title: error.code,
                description: error.message,
                backgroundColor: "red.600",
              });
            });
        }}
      >
        Logout
      </Button>
      {/*<Fab*/}
      {/*  onPress={recording ? stopRecording : startRecording}*/}
      {/*  renderInPortal={false}*/}
      {/*  shadow={2}*/}
      {/*  size="lg"*/}
      {/*/>*/}
    </Box>
  );
}
