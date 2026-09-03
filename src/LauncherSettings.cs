namespace LauncherConfig
{
    // Ponto unico de configuracao do launcher PrimeOT.
    // Trocar URLs aqui quando o dominio + HTTPS entrarem — sem mexer no resto do codigo.
    public static class LauncherSettings
    {
        public const string AppName = "PrimeOT"; // provisorio

        // Manifesto de update (GitHub, HTTPS) — R-L1.
        public const string LauncherConfigUrl =
            "https://raw.githubusercontent.com/ReginaldoMedeiros/ot-launcher/main/launcher_config.json";

        // Endpoint de login do servidor (POST {type:"cacheinfo"} -> playersonline).
        // Alpha/Tailscale: HTTP no IP atual. Vira HTTPS+dominio depois.
        public const string OnlinePlayersUrl = "http://100.92.208.63/login.php";

        // Vitrine / links.
        public const string WebsiteUrl     = "http://100.92.208.63/";
        public const string DonateUrl      = "http://100.92.208.63/?donations";
        public const string DiscordUrl     = "https://discord.gg/PLACEHOLDER";
        public const string NewsArchiveUrl = "http://100.92.208.63/?news/archive";

        // Fase 2 — endpoint JSON unificado do MyAAC.
        public const string LauncherApiUrl = "http://100.92.208.63/launcher.php";
    }
}
