import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.lightGreen),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Flutter To-do List'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}


class _MyHomePageState extends State<MyHomePage> {
  final TextEditingController _controllername = TextEditingController();
    final TextEditingController _controllerdata = TextEditingController();



  void showMyDialog() async {
  return showDialog<void>(
        context: context,
        builder: (BuildContext context) => AlertDialog(
          title: const Text('Adicionar Tarefa'),
          content: const Text('Adicionar tarefa a To-do List'),
          actions: <Widget>[
          TextField(
            controller: _controllername,
            decoration: const InputDecoration(
            border: OutlineInputBorder(),
            labelText: 'Nome do seu post'
              ),
            ),
            TextField(
            controller: _controllerdata,
            decoration: const InputDecoration(
            border: OutlineInputBorder(),
            labelText: 'Diga o que você está pensando...'
              ),
            ),
            Row(
              children: [
              TextButton(
                onPressed: () => Navigator.pop(context, 'Cancel'),
                child: const Text('Cancel'),
              ),
              TextButton(
                onPressed: () => Navigator.pop(context, 'OK'),
                child: const Text('OK'),
              ),
              ],
            )
          ],
        ),
      );
}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: const Center(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        child: Column(
          verticalDirection: VerticalDirection.down,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
              Text("Últimas tarefas",
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 26, height: 2),)
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
                    onPressed: () {showMyDialog();},
                    child: const Icon(Icons.add),
                    ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
