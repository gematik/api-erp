using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;

class Program {
    static void Main() {
        //subscriptionId und bearertoken aus VAU-Request /Subcription extrahieren
        CreateSocket("df694c098c2fb373524150461cfd9d23",
            "Bearer eyJhbGciOiJFUzI1NiJ9.CnsKInN1YnNjcmlwdGlvbklkIjogImRmNjk0YzA5OGMyZmIzNzM1MjQxNTA0NjFjZmQ5ZDI…");
    }

    private static void CreateSocket(string subscriptionId, string bearertoken) {
        var _websocketObj = new ClientWebSocket();
        _websocketObj.Options.SetRequestHeader("Authorization", bearertoken);
        //url RU: "wss://subscription-ref.zentral.erp.splitdns.ti-dienste.de" und PU: "wss://subscription.zentral.erp.splitdns.ti-dienste.de"
        _websocketObj.ConnectAsync(new Uri("wss://subscription-ref.zentral.erp.splitdns.ti-dienste.de/subscription"), CancellationToken.None)
            .Wait();

        if (_websocketObj.State != WebSocketState.Open) {
            throw new Exception("Websocket ist nicht geöffnet");
        }

        {
            var bind = $"bind: {subscriptionId}";
            _websocketObj.SendAsync(new ArraySegment<byte>(Encoding.UTF8.GetBytes(bind)), WebSocketMessageType.Text, true, CancellationToken.None)
                .Wait();
            Console.Out.WriteLine($"Websocket-Bind: {bind}");

            var buffer = new ArraySegment<byte>(new byte[2048]);
            WebSocketReceiveResult wsr = _websocketObj.ReceiveAsync(buffer, CancellationToken.None).Result;
            var res = Encoding.UTF8.GetString(buffer.Array, buffer.Offset, wsr.Count);
            Console.Out.WriteLine($"Websocket-Bound: {res}");
        }

        while (true) {
            var buffer = new ArraySegment<byte>(new byte[2048]);
            WebSocketReceiveResult wsr = _websocketObj.ReceiveAsync(buffer, CancellationToken.None).Result;
            // ReSharper disable once AssignNullToNotNullAttribute
            var res = Encoding.UTF8.GetString(buffer.Array, buffer.Offset, wsr.Count);
            if (wsr.Count > 0) {
                Console.Out.WriteLine($"Websocket-Empfangen: {res} ({wsr.Count} Bytes) -> es liegen neue Nachrichten bereit!");
            }
        }
    }
}