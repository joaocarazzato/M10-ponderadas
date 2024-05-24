import 'package:flutter/material.dart';
import 'package:flutter_app/api/firebase_api.dart';
import 'package:flutter_app/api/storage_api.dart';
import 'package:flutter_app/pagina_camera.dart';
import 'package:flutter_app/registro.dart';
import 'package:http/http.dart' as http;
import 'package:firebase_core/firebase_core.dart';
import 'dart:convert';

final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();
var fCMToken = '';
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  fCMToken = await FirebaseApi().initNotifications();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      navigatorKey: navigatorKey,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(),
      routes: {
        PaginaCamera.route: (context) => const PaginaCamera()
      },
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});


  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final TextEditingController _controlleruser = TextEditingController();
  final TextEditingController _controllerpass = TextEditingController();
  
  String _resultadorequest = '';

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      body: Center(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        child: Column(
          // Column is also a layout widget. It takes a list of children and
          // arranges them vertically. By default, it sizes itself to fit its
          // children horizontally, and tries to be as tall as its parent.
          //
          // Column has various properties to control how it sizes itself and
          // how it positions its children. Here we use mainAxisAlignment to
          // center the children vertically; the main axis here is the vertical
          // axis because Columns are vertical (the cross axis would be
          // horizontal).
          //
          // TRY THIS: Invoke "debug painting" (choose the "Toggle Debug Paint"
          // action in the IDE, or press "p" in the console), to see the
          // wireframe for each widget.
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'Bem vindo!',
              style: TextStyle(height: 3, fontSize: 30),
            ),
            const Text(
              'Faça seu login!',
              style: TextStyle(fontSize: 16),
            ),
            TextButton(
                onPressed: () {
                  Navigator.push(context, MaterialPageRoute(builder: (context) => const PaginaRegistro()));
                  },
                child: const Text('Não possui conta?',
                style: TextStyle(fontSize: 14)),
              ),
            TextField(
            controller: _controlleruser,
            decoration: const InputDecoration(
            border: OutlineInputBorder(),
            labelText: 'Usuário'
              ),
            ),
            TextField(
            controller: _controllerpass,
            decoration: const InputDecoration(
            border: OutlineInputBorder(),
            labelText: 'Senha'
              ),
            ),
            Text(_resultadorequest,
            style: const TextStyle(
        color: Color.fromARGB(255, 252, 1, 1),
      )),
            // ElevatedButton(onPressed: (){
            //   Navigator.push(context, MaterialPageRoute(builder: (context) => const PaginaCamera()));
            // }, child: const Text("Clique aqui"))
            ElevatedButton(onPressed: () async{
              print("TOKEN REQUEST!!!!: $fCMToken");
          var resposta = await http.post(Uri.parse("http://10.0.2.2:8000/auth/login"), 
          headers: <String, String>{
            'Content-Type': 'application/json; charset=UTF-8',
          },
          body: jsonEncode({
            'username': _controlleruser.text, 
            'password': _controllerpass.text,
            'token': fCMToken
          })
          );
          _resultadorequest = '';
          if (resposta.statusCode == 200) {
            print(jsonDecode(resposta.body)['id']);
            StorageApi().saveId(jsonDecode(resposta.body)['id']);
            // ignore: use_build_context_synchronously
            Navigator.push(context, MaterialPageRoute(builder: (context) => const PaginaCamera()));
          }
          else {
            setState(() {
            if (resposta.statusCode != 500) {

            var respostaprocessada = jsonDecode(resposta.body);
            _resultadorequest = respostaprocessada['detail'];
            }
            else {
              _resultadorequest = "Ocorreu um erro.";
            }
          });
          }
          },  child: const Text("Entrar"))
          ],
        ),
      )
    );
  }
}
