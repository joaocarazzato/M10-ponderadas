import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_app/main.dart';
import 'dart:convert';

class PaginaRegistro extends StatefulWidget {
  const PaginaRegistro({super.key});

  @override
  State<PaginaRegistro> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<PaginaRegistro> {
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
      appBar: AppBar(title: const Text("Pagina de Registro"),
      backgroundColor: Theme.of(context).colorScheme.inversePrimary),
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
              'Registro',
              style: TextStyle(height: 3, fontSize: 30),
            ),
            const Text(
              'Faça seu registro!',
              style: TextStyle(fontSize: 15),
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
          var resposta = await http.post(Uri.parse("http://10.0.2.2:8000/auth/users"), 
          headers: <String, String>{
            'Content-Type': 'application/json; charset=UTF-8',
          },
          body: jsonEncode({
            'username': _controlleruser.text, 
            'password': _controllerpass.text
          })
          );
          _resultadorequest = '';
          if (resposta.statusCode == 200) {
            // ignore: use_build_context_synchronously
            Navigator.push(context, MaterialPageRoute(builder: (context) => const MyApp()));
          }
          else {
            setState(() {
            var respostaprocessada = jsonDecode(resposta.body);
            _resultadorequest = respostaprocessada['detail'];
          });
          }
          },  child: const Text("Registrar"))
          ],
        ),
      )
    );
  }
}