import { signOut } from "@firebase/auth";
import {Button, Center, Text, useToast} from "native-base";
import {auth} from "../../firebase";

export function HomePage(){
    const toast = useToast();

    return (
        <Center
            _dark={{ bg: "blueGray.900" }}
            _light={{ bg: "blueGray.50" }}
            px={4}
            flex={1}
        >
            <Text>This is Home Page</Text>
            <Button onPress={() => {signOut(auth).then().catch((error) => {
                toast.show({title: error.code, description: error.message, backgroundColor: "red.600"});
            })}}>Logout</Button>
        </Center>
    );
}
