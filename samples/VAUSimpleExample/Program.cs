using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;

namespace VAUSimpleExample {
    class Program {
        static void Main() {
            //Beispiel der VAU aus gemSpec_Krypt_V2.19.0.pdf Seite 98
            VAUFixed.DemoBspAusGemSpecCrypt();

            //VAU Bsp für TITUS Download erezept

            //TODO aus TITUS einfügen: accesscode, taskid und apoBearerKey
            const string accesscode = "6152f3a653092e79ce4a2e65c2f0c01d50bd144fcbebba25d60d11b60d793323";
            const string taskid = "b4f0ee8d-306c-11b2-8bae-75f4f3ff4c92";
            const string apoBearerKey =
                "eyJhbGciOiJCUDI1NlIxIiwidHlwIjoiYXQrSldUIiwia2lkIjoicHVrX2lkcF9zaWcifQ.eyJzdWIiOiJlVk1pTGxWOVU4dGFrUnVPUDg5TFpiZUczVi1oRWV6VlgyQ1RfRXVhT21nIiwicHJvZmVzc2lvbk9JRCI6IjEuMi4yNzYuMC43Ni40LjU0Iiwib3JnYW5pemF0aW9uTmFtZSI6IjMtU01DLUItVGVzdGthcnRlLTg4MzExMDAwMDExNjk4MCIsImlkTnVtbWVyIjoiMy1TTUMtQi1UZXN0a2FydGUtODgzMTEwMDAwMTE2OTgwIiwiYW1yIjpbIm1mYSIsInNjIiwicGluIl0sImlzcyI6Imh0dHBzOi8vaWRwLnplbnRyYWwuaWRwLnNwbGl0ZG5zLnRpLWRpZW5zdGUuZGUiLCJnaXZlbl9uYW1lIjoiUm9sZiIsImNsaWVudF9pZCI6ImVSZXplcHRBcHAiLCJhdWQiOiJodHRwczovL2VycC50ZWxlbWF0aWsuZGUvbG9naW4iLCJhY3IiOiJnZW1hdGlrLWVoZWFsdGgtbG9hLWhpZ2giLCJhenAiOiJlUmV6ZXB0QXBwIiwic2NvcGUiOiJvcGVuaWQgZS1yZXplcHQiLCJhdXRoX3RpbWUiOjE2MTkyNDYwMjEsImV4cCI6MTYxOTI0NjMyMSwiZmFtaWx5X25hbWUiOiJDw7ZyZGVzIiwiaWF0IjoxNjE5MjQ2MDIxLCJqdGkiOiJhZjk3MDQ1MmQwMDBiMDM2In0.JD7qLbNRDOiAWlU_3wqey2FNrz3lNJB5ZYz4b6BWb4ZzyrjSID56GltUG_yiaiBpgFPrppNgckBw7jXA8DcBwg";

            string content = $@"POST /Task/{taskid}/$accept?ac={accesscode} HTTP/1.1
Host: fd.erezept-instanz1.titus.ti-dienste.de
Authorization: Bearer {apoBearerKey}
Content-Type: application/fhir+xml
User-Agent: x
Accept: application/fhir+xml;charset=utf-8

";

            var vau = new VAU();

            string requestid = VAU.ByteArrayToHexString(vau.GetRandom(16));
            string aeskey = VAU.ByteArrayToHexString(vau.GetRandom(16));
            string p = $"1 {apoBearerKey} {requestid.ToLowerInvariant()} {aeskey.ToLowerInvariant()} {content}";

            Console.Out.WriteLine($"{requestid.ToLowerInvariant()} {aeskey.ToLowerInvariant()}");

            var gesamtoutput = vau.Encrypt(p);

            var client = new HttpClient {
                BaseAddress = new Uri("https://fd.erezept-instanz1.titus.ti-dienste.de"), Timeout = TimeSpan.FromSeconds(30)
            };
            client.DefaultRequestHeaders.ExpectContinue = false;

            HttpResponseMessage response = client.PostAsync("VAU/0",
                    new ByteArrayContent(gesamtoutput)
                        {Headers = {ContentType = MediaTypeHeaderValue.Parse("application/octet-stream")}})
                .Result; // Blocking call!    

            if (response.IsSuccessStatusCode) {
                Console.Out.WriteLine("VAU Request erfolgreich");
                foreach (var header in response.Headers) {
                    Console.Out.WriteLine($"{header.Key}={string.Join(",", header.Value)}");
                }
                var encryptedResponse = response.Content.ReadAsByteArrayAsync().Result;

                var decrypt = vau.DecryptWithKey(encryptedResponse, VAU.HexStringToByteArray(aeskey));
                var xml = Encoding.UTF8.GetString(decrypt);

                Console.Out.WriteLine($"entschlüsselter Response={xml}");
            } else {
                Console.WriteLine($"{(int) response.StatusCode} ({response.ReasonPhrase})");
                Console.Out.WriteLine($"Response body: {response.Content.ReadAsStringAsync().Result}");
            }
        }
    }
}