import {TapGestureHandler, FlingGestureHandler, State, Directions} from 'react-native-gesture-handler';
import {useEffect, useState} from "react";
import {Center, Heading, ScrollView, useToast, View} from "native-base";
import axios from "axios";

export function SlidesPage({ route, navigation }: any){
    const { recording } = route.params;
    const [mainText, setMainText] = useState('Flashcards are loading...');
    const [node, setNode] = useState<any>();
    const [tree, setTree] = useState<any>();
    const toast = useToast();

    useEffect(() => {
        axios.post('https://src-usbebnquka-ue.a.run.app/get_visualization_url', {
            url: recording.url
        }).then((res) => {
            let json = JSON.parse(res.data[Object.keys(res.data)[0]]);
            setNode(json);
            setTree(res.data);
            setMainText(json["front"])
        }).catch((err) => {
            console.log(err);
            toast.show({title: "Error", description: "There was an error getting the slides. Please try again.", backgroundColor: "red.500"})
        })
    }, [])

    return (
        <FlingGestureHandler direction={Directions.LEFT} onHandlerStateChange={({nativeEvent}) => {
            if (nativeEvent.state === State.ACTIVE) {
                if (node["first"]){
                    setNode(tree[node["first"]]);
                }
            }
        }}>
            <FlingGestureHandler direction={Directions.RIGHT} onHandlerStateChange={({nativeEvent}) => {
                if (nativeEvent.state === State.ACTIVE) {
                    console.log("swiped right");
                    if (node["second"]){
                        setNode(tree[node["second"]]);
                    }
                }
            }
            }>
                <TapGestureHandler onHandlerStateChange={({nativeEvent}) => {
                    if (nativeEvent.state === State.ACTIVE) {
                        if (mainText === node["front"]){
                            setMainText(node["back"]);
                        }
                        else {
                            setMainText(node["front"]);
                        }
                    }
                }}>
                        <View height={"100%"} display={"flex"} alignContent={"center"} alignItems={"center"} flexDirection={"column"} justifyContent={"center"} px={16} py={16}>
                            <Heading>Flashcards</Heading>
                            <ScrollView contentContainerStyle={{ flexGrow: 1, justifyContent: 'center' }}>
                                <Center>
                                    <Heading textAlign={"justify"}>{mainText}</Heading>
                                </Center>
                            </ScrollView>
                        </View>

                </TapGestureHandler>
            </FlingGestureHandler>
        </FlingGestureHandler>
    );
}
