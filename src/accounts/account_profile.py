

class AccountProfile:

    def __init__(
        self,
        name_first: str = None,
        name_last: str = None,
        bio_descript: str = None,
        location: str = None
    ) -> None:
        
        if name_first:
            self.name_first = name_first
        if name_last:
            self.name_last = name_last
        if bio_descript:
            self.bio_descript = bio_descript.encode('utf-8')
        if location:
            self.location = location


class ArtistProfile(AccountProfile):

    def __init__(
        self,
        name_first: str = None,
        name_last: str = None,
        bio_descript: str = None,
        location: str = None,
        website: str = None,
        twitter_username: str = None
    ) -> None:

        super().__init__(
            name_first=name_first,
            name_last=name_last,
            bio_descript=bio_descript,
            location=location
        )


class UserProfile(AccountProfile):
    pass
