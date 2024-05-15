import { View, Text } from "react-native";
import MyStyles from "../../styles/MyStyles";

const Register = () => {
    return (
        <View style={[MyStyles.container, MyStyles.margin]}>
            <Text style={MyStyles.subject}>ĐĂNG KÝ NGƯỜI DÙNG</Text>
        </View>
    );
}

export default Register;