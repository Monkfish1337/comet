# SeriousSportSync

Comet can resolve a SeriousSportSync event into title variants and search its
configured title-based scrapers for that event. SeriousSportSync remains the
catalog and metadata add-on; Comet supplies torrent discovery and playback.

## Server setup

The Comet operator must explicitly allow the SeriousSportSync host. This keeps
user-supplied manifest URLs from becoming unrestricted server-side requests.

```env
SERIOUSSPORTSYNC_ALLOWED_HOSTS=serioussportsync:7000
```

Use a comma-separated list when more than one public or Docker-network address
must be accepted. Entries include the port when the URL includes one.

## User setup

1. Copy the personal manifest URL from the SeriousSportSync account page.
2. Open Comet's configure page and expand **SeriousSportSync**.
3. Paste the manifest URL, configure the desired Comet scrapers and debrid
   service, then install Comet.
4. Keep SeriousSportSync installed as the catalog add-on.

The manifest URL contains a private account token. Comet uses its matching
token-scoped `search-context` endpoint to obtain the event title aliases, year,
and date. Regenerating the SeriousSportSync token invalidates the old URL.

Direct title-search scrapers such as Prowlarr, Jackett, Zilean, Nyaa, BitMagnet,
and DMM can use these event queries. Add-on forwarding sources that only accept
IMDb/TMDB/Kitsu identifiers may not support SeriousSportSync event IDs.
